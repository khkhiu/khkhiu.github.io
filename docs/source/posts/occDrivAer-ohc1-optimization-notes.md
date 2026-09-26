---
title: "Optimizing OpenFOAM's occDrivAer Case for the APAC HPC-AI Competition 2026"
date: 2026-09-25
tags: [hpc, openfoam, cfd, decomposition, mpi]
---

# Optimizing OpenFOAM's occDrivAer Case for the APAC HPC-AI Competition

*Published: 2026-09-25*


**TL;DR:** Before spending any competition compute hours on `occDrivAerStaticMesh`, we pulled the submission spreadsheets from the original OpenFOAM HPC Challenge (OHC-1) to see what the fastest 4-node runs actually did. Every team that reported a method used the same combination: `hierarchical` decomposition + `RCM` renumbering. Nobody switched to a graph partitioner (`scotch`/`kahip`) to win. That means the method choice for this case is already settled, the leverage left is in *tuning the numbers* (decomposition coefficients, rank count, binding), not in *changing the method*.

```{note}
This is a working-notes-style writeup from a live preparation session ahead of
the APAC HPC-AI 2026 Competition, not a controlled benchmark. The submission
comparison below is read directly from OHC-1's public spreadsheets; we have not
yet reproduced any of those numbers ourselves.
```

## Background

`occDrivAerStaticMesh` is the OpenFOAM task for the APAC HPC-AI 2026 Competition, run on either NCI **Gadi** or NSCC **ASPIRE-2A**, with a practice cluster (**Vanda**, Sapphire Rapids, PBS Pro) for iteration before spending scored-cluster hours. The case itself is drawn from the **OpenFOAM HPC Challenge (OHC-1)**: 12 organizations, 237 submitted data points, single-node up to 256-node runs, 25 CPU models, presented at the 20th OpenFOAM Workshop in Vienna.

**occDrivAer** = **o**pen-**c**losed **c**ooling **DrivAer** — the notchback Ford Open Cooling DrivAer (OCDA) geometry, with cooling inlets sealed and wheels static, a full car body with a genuinely complex underbody and engine-bay geometry rather than a simplified benchmark shape. The competition's scored task uses the unmodified **65M-cell coarse mesh**, `simpleFoam` (steady RANS, SIMPLE, fixed inner iterations), at 40/80/150 iterations for 1/2/4 nodes.

Two headline findings from the OHC-1 paper set the frame for everything below:
- **Single-node performance is memory-bandwidth-bound** — consistent with OpenFOAM's sparse linear-algebra kernels.
- **Multi-node performance is communication-bound**, with a practical strong-scaling floor around **~10,000 cells/core**, below that, communication cost exceeds compute.

Both point the same direction: for this case, decomposition quality and cache reuse matter more than raw FLOPs.

## The investigation

### Decomposition: why `hierarchical`, not a graph partitioner

`decomposePar` decides which MPI rank owns each cell — it controls processor-boundary size and load balance.

| Method | Basis | Load balance | Comm. minimization | Tunable to hardware | Decompose cost |
|---|---|---|---|---|---|
| **hierarchical** | Geometric bisection (slab cuts along x/y/z) | Good on regular meshes | Not directly optimized | **Yes** — explicit `n (nx ny nz)` | Very low |
| **scotch** | Graph partitioning, multilevel | Good, self-balancing | Yes | No | Moderate |
| **metis** | Graph partitioning (Karypis & Kumar) | Good | Yes | No | Moderate |
| **kahip** | Graph partitioning, typically highest quality | Best | Best | No | Highest |

`occDrivAer`'s refinement is a set of nested, axis-aligned boxes around a compact car-shaped region inside a much larger, mostly-uniform far-field — a shape geometric bisection handles evenly. `hierarchical` is also the *only* method where the decomposition shape can be deliberately aligned to node/socket/core topology, rather than accepting whatever a graph partitioner produces.

One caveat we didn't expect going in: `hierarchical` balances by **cell count**, not **face count**. The dense car/wake region is geometrically thin, so cuts through it produce disproportionately more processor-boundary faces per cell than cuts through the empty far-field — invisible if only per-rank cell counts are checked.

```bash
grep -A 30 "Processor" logFiles/10_decomposePar.log | grep -i "faces\|cells"
```

### Renumbering: RCM is already the default, and already correct

Decomposition decides *which rank* owns a cell; renumbering decides the *in-memory ordering* of cells within a rank. Different problems — one minimizes inter-rank communication, the other minimizes cache misses during per-rank computation.

**RCM (Reverse Cuthill-McKee)**: treat the per-rank mesh as a graph (cells as nodes, shared faces as edges), do a breadth-first traversal from a low-degree starting node so geometrically adjacent cells get numerically close indices, then reverse that ordering (empirically better fill-in behavior for iterative solvers, at no extra cost). The effect: the sparse matrix's nonzero pattern collapses into a narrow band around the diagonal, sharply reducing cache misses on every matrix-vector operation, with zero change to the underlying math or result.

It's already in the pipeline correctly — RCM is `renumberMesh`'s **default**, no flag needed, and order matters: renumbering runs *after* decomposition (`decomposePar → restore0Dir → renumberMesh -parallel`), so each rank only optimizes its own local subdomain.

```bash
grep -i "renumber\|bandwidth" logFiles/20_renumberMesh.log
```

This matters more here than in a typical case, precisely *because* the workload is bandwidth-bound: RCM improves reuse of bytes already moved from RAM, it doesn't reduce total bytes moved, which is exactly the right lever for this bottleneck.

## Result: what the fastest OHC-1 submissions actually used

We read the `Simulations` sheet of the four OHC-1 submissions whose 65M-coarse-mesh hardware-track numbers are this competition's own sanity-check reference (Huawei, Wikki, UniBwM, BAW), for their 4-node configuration:

| Team | Hardware | Nodes | Cores | Decomp. method | Renumber | s/iteration |
|---|---|---|---|---|---|---|
| Huawei | LX2 (ARM) | 4 | 1024 | `hierarchical` | `RCM` | 1.247 |
| BAW | AMD EPYC 9654 | 4 | 768 | `hierarchical` | `RCM` | 1.425 |
| Wikki | AMD EPYC 7763 | 4 | 512 | `hierarchical` | `RCM` | 3.467 |
| Wikki | Intel Xeon 8480+ | 4 | 448 | `hierarchical` | `RCM` | 2.520 |
| UniBwM | AMD EPYC 7662 | 4 | 512 | "standard"* | "standard"* | 6.817 |

\* Almost certainly the case-provided default, i.e. also hierarchical/RCM, not a genuinely different method.

**Every team that specified a method used the same combo.** Nobody switched to `scotch`/`kahip` to win their scored run. Caveats worth keeping in mind: all four ran **OpenFOAM v2412** (this competition requires v2512) at **2000 iterations** (not this competition's 40/80/150 scaling scheme) — so this validates *method choice*, not a raw performance target we can compare our own numbers against directly.

## Why it works

Both results trace back to the same root cause: this is a **memory-bandwidth-bound workload**, not a compute-bound one. `simpleFoam`'s dominant per-iteration cost is the GAMG multigrid solve for pressure — sparse, irregular-access-pattern, characteristically limited by memory bandwidth and cache behavior rather than FLOPs. That's why:

- **Decomposition** wins by minimizing communication and letting shape be aligned to hardware, not by any raw partition-quality metric a graph partitioner would optimize harder for.
- **RCM renumbering** wins by improving cache reuse of data already fetched from RAM — a bandwidth-bound kernel benefits disproportionately from a technique that changes *nothing* about total bytes moved, only how well those bytes get reused before eviction.
- OHC-1's own analysis backs this reading: it explicitly discounted hyperthreads, counting only physical cores when computing scaling metrics — consistent with a bandwidth-bound workload where filling every hardware thread adds shared-bus contention without adding memory channels.

Applying the ~10,000 cells/core practical floor from OHC-1 to our fixed 65M-cell mesh:

| Nodes | ~128 cores/node (Aspire2A-class) | Cells/core |
|---|---|---|
| 1 | 128 | ~508,000 |
| 2 | 256 | ~254,000 |
| 4 | 512 | ~127,000 |

All comfortably inside the "good" zone (100k–1M cells/core) — cells/core is not the binding constraint at 4 nodes on this mesh, so there's headroom before communication overhead dominates, and headroom to spend on the tuning below rather than a method change.

## Known issues and open items

- **Face-count imbalance is a real risk, not yet measured on our own runs.** We know cell-count balance can mask face-count imbalance in the car/wake region (see the `grep` above); we haven't yet run it against our own `decomposePar` logs to confirm whether it's actually present at our target rank counts.
- **Physical-core vs. full-SMT rank count is an assumption, not a measured result, for this case specifically.** OHC-1's methodology discounts hyperthreads, and a companion post found a 17% win from disabling SMT on a related Zen3/`xcnf` run — but that was a different cluster and a different rank-count regime; we haven't A/B'd it on Vanda/Aspire2A-class hardware for occDrivAer yet.
- **The submission comparison above is a method validation, not a performance target.** Different OpenFOAM version (v2412 vs. our required v2512) and a different iteration count (2000 vs. our 40/80/150 scaling scheme) mean the `s/iteration` column is not something we can benchmark our own runs against directly.
- **Compiler flags and MPI transport tuning (`--mca pml ucx`) remain untested** for this case — expected to be a smaller lever than decomposition/renumbering given the bandwidth-bound profile, but not yet measured either way.

## Next up

With method choice settled, the next round of testing is about the *numbers*, not the *method*:

1. Re-derive `nHierarchical` from actual node/socket/core topology (coarsest split on the long flow axis, matching node count) rather than an extrapolated ratio, and diff-check the resulting decomposition's face balance, not just cell balance.
2. Run the physical-core-vs-full-SMT comparison directly on this case, on the practice cluster, before committing scored-cluster hours to either assumption.
3. Confirm RCM is doing real work at our actual decomposition (`grep` the renumber log) rather than trusting that "it's the default" is sufficient on its own.
4. Only after 1–3: layer in compiler flags (`-march=znver3`/`-march=sapphirerapids` as appropriate) and MPI binding/transport tuning, and treat any gain there as a secondary effect on top of a validated decomposition.

---

*Setup: `occDrivAerStaticMesh`, OpenFOAM v2512 (required for this competition), coarse mesh (65M cells), APAC HPC-AI 2026 Competition OpenFOAM task, method comparison drawn from OHC-1 public submission data (Huawei, Wikki, UniBwM, BAW).*
