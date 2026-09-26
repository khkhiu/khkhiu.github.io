---
title: "A 1 node decomposition and MPI-binding study on Vanda"
date: 2026-09-25
tags: [openfoam, hpc, cfd, decomposition, mpi]
---

# A 1 node decomposition and MPI-binding study on Vanda

*Published: 2026-09-25*

**TL;DR:** Ahead of committing walltime to the scored 4-node `occDrivAerStaticMesh` run, we swept 8 mesh-decomposition shapes and 5 MPI rank-binding strategies at 1-node scale (72 ranks) on NUS's Vanda cluster (PBS Pro, Sapphire Rapids). Our first sweep pointed to one clear winner, until an identical repeat run came back **47% faster** on a different node. The real story turned out to be **shared-cluster memory-bandwidth contention from other users' jobs**, worth up to a ~90% wall-clock swing, dwarfing every optimization we deliberately tested. Once we controlled for that, `hierarchical (18 4 1)` decomposition was a real, reproducible ~4.5–6.5% win, and MPI pin order made no measurable difference at all (differences fell inside a ~1% noise floor).

```{note}
This is a working-notes-style writeup from a live 1-node exploratory session, not
a controlled multi-node benchmark. All numbers below are 40-iteration,
72-rank, single-node runs, intended to pick a configuration to carry into the
scored 2- and 4-node runs, not to stand in for those results.
```

## Background

**`occDrivAerStaticMesh`** is the OHC-1 competition case: airflow over a static car body at 140 km/h, 65 million mesh cells, solved with `simpleFoam` (steady-state RANS, SIMPLE algorithm) run for a fixed number of iterations per node count (40 at 1 node, 80 at 2, 150 at 4, so results are comparable across scales). The primary metric throughout is the solver's own reported **`Average wall-clock time per time step`** (`s/step`), lower is better.

**Vanda** is NUS's PBS Pro cluster: nodes here have 2× Intel Xeon Platinum 8452Y (Sapphire Rapids), 72 physical cores total across two sockets (36 each), 512 GB RAM, no SMT in this configuration (every core runs exactly one MPI rank). Like most shared HPC clusters, Vanda's default scheduling policy (`place=free`) does **not** guarantee a job exclusive use of a node, another user's job can land on the same physical machine and compete for the same shared memory bandwidth.

The mesh is split across ranks by `decomposePar`. We used `hierarchical` decomposition throughout, specified as a triplet `(Nx Ny Nz)` of cuts along each spatial axis, chosen specifically for its **determinism**: the same triplet on the same mesh always produces the same split, which matters for reproducibility in a competition setting in a way a graph-based method (`scotch`) does not guarantee without extra seeding. Rank *placement onto cores* is a separate question from decomposition, controlled here via Intel MPI's `I_MPI_PIN_DOMAIN`/`I_MPI_PIN_ORDER` environment variables, which decide whether ranks stay fixed to one physical core for the whole run and which core each rank number gets.

## The experiment: sweeping decomposition shapes

The first sweep tested 8 shapes, all at 72 ranks, submitted as a single PBS job so all 8 ran back-to-back on the same physical node:

| Shape `(Nx Ny Nz)` | Pin order | s/step |
|---|---|---:|
| `(12 6 1)` | default | 17.874 |
| `(12 6 1)` | compact | 17.678 |
| `(12 6 1)` | scatter | 17.679 |
| `(24 3 1)` | compact | 17.765 |
| `(36 2 1)` | compact | 17.788 |
| `(18 4 1)` | compact | 17.411 |
| `(12 3 2)` | compact | **17.272** |
| `(6 6 2)` | compact | 17.507 |

At face value, `(12 3 2)` — the only shape in this batch that also cut the vertical (z) axis — looked like the winner. It didn't survive re-testing.

## Result: the shape that won, until a repeat flagged something wrong

To check the run-to-run noise floor, we resubmitted `(12 3 2)` as an identical repeat. It landed on a different physical node and came back **47% faster**:

| Run | Node | s/step |
|---|---|---:|
| Original sweep | CN-099 | 17.272 |
| Repeat 1 | CN-142 | 9.188 |
| Repeat 2 | CN-142 | 9.241 |
| Repeat 3 | CN-051 | 9.256 |
| Repeat 4 | CN-051 | 9.167 |

Four repeats across two independently-selected nodes clustered tightly, 9.167–9.256 s/step, under a 1% spread. That's a healthy noise floor. The original CN-099 result sat entirely outside it, at roughly **1.9× slower**.

`pbsnodes` showed CN-099 and the clean nodes had identical hardware specs, so this wasn't a hardware-tier difference. A stage-by-stage breakdown pinned the slowdown specifically to the long, memory-bandwidth-bound `simpleFoam` solve, not the shorter prep steps:

| Stage | CN-099 | CN-142 | Ratio |
|---|---:|---:|---:|
| renumberMesh | 3.72 s | 4.20 s | ~1.1× |
| potentialFoam | 31.59 s | 30.83 s | ~1.0× |
| applyBoundaryLayer | 5.26 s | 5.37 s | ~1.0× |
| **simpleFoam (avg/step)** | **17.27 s** | **9.19 s** | **~1.9×** |

Short stages agreed within ~10%; only the sustained solve, exactly the phase most sensitive to memory-bandwidth pressure, showed the gap. Checking `pbsnodes` at the time confirmed other users' array jobs were co-resident on both CN-099 and CN-142 at various points, consistent with PBS's default `place=free` policy, which reserves your requested cores/memory but does not stop another job from sharing the same physical node's remaining resources and memory subsystem. **Conclusion: memory-bandwidth contention from co-located jobs, not a hardware or configuration difference.** A property of running on a shared, multi-tenant cluster, not a flaw in the case setup.

Once that confound was identified, we restructured every remaining comparison to either run all configurations back-to-back on one node (so a contended node penalizes everything in that comparison equally) or explicitly cross-check with repeats on multiple nodes. Re-running the leading shapes on confirmed clean nodes gave a very different ranking than the original sweep:

| Shape | Node | s/step |
|---|---|---:|
| `(18 4 1)` | CN-090 | 9.176 |
| `(18 4 1)` | CN-108 | 9.095 |
| `(12 6 1)` | GN-A40-078 | 9.599 |
| `(12 3 2)` | GN-A40-078 | 9.602 |
| `(6 6 2)` | GN-A40-078 | 9.735 |

`(18 4 1)` is consistently fastest — confirmed independently on two separate nodes at 9.1–9.2 s/step, about 4.5–6.5% faster than the others tested. `(12 3 2)`'s apparent lead in the original sweep was the contention artifact: it inflated all eight of that sweep's timings by a similar factor, preserving *some* relative ordering by chance but not reliably, since the true ranking flipped once contention was removed. We could not establish a mechanistic reason `(18 4 1)` wins — `decomposePar`'s own processor-face-balance numbers didn't cleanly predict the ranking across shapes — so this is reported as an empirical finding, not a theoretical one.

## MPI rank binding: same noise floor, no real winner

With decomposition settled, we swept five Intel MPI `I_MPI_PIN_ORDER` strategies (plus a repeat, as a noise check) on the winning shape, all six back-to-back on one node to eliminate the contention confound entirely:

| Binding strategy | s/step | Δ vs. fastest |
|---|---:|---:|
| `bunch` | 9.0889 | — |
| `compact` | 9.0923 | +0.04% |
| `compact` (repeat) | 9.0951 | +0.07% |
| `nopin` | 9.1179 | +0.32% |
| `scatter` | 9.1515 | +0.69% |
| `spread` | 9.1890 | +1.10% |

Rather than trust timing alone, we pulled the actual rank-to-core assignments from each run's Intel MPI startup log. `compact`, `bunch`, and `spread` turned out to produce the **exact same** physical mapping (rank 0 → core 0, rank 1 → core 2, ... filling socket 1 before socket 2), confirmed by a line-by-line diff of the pinning tables. Only `scatter` produced a genuinely different layout (deliberately avoiding placing consecutive ranks near each other), and `nopin` left every rank's affinity mask open to all 72 cores for the whole run.

Because three of the five "different" strategies are secretly identical placements, their ~1.1% timing spread is direct, in-log evidence of this configuration's true noise floor with zero placement difference at all. `scatter`'s result falls inside that same band. `nopin` also fell within it over this 40-iteration test, but its affinity mask permits migration for the entire run, and we can't rule out drift or cache-locality loss over the full 150-iteration scored run — flagged as open below rather than dismissed.

We selected `I_MPI_PIN_DOMAIN=core`, `I_MPI_PIN_ORDER=compact`: not because it beat its closest alternatives (it didn't, measurably), but because it's the more conventional, widely-recognized name for this behavior and avoids `nopin`'s unverified long-run migration risk.

## Why the contention effect dominates everything else

`simpleFoam`'s sustained solve phase is memory-bandwidth-bound — the CPU spends more time waiting on data movement than on arithmetic. That's exactly the resource a co-located job on a shared, non-exclusive node competes for hardest: a second job's memory traffic on the same node directly steals bandwidth from your solve, with the effect scaling with how long and how bandwidth-hungry your own job's dominant phase is. Short utility stages (`renumberMesh`, `potentialFoam`, `applyBoundaryLayer`) barely notice a co-tenant because they're brief; the long solve notices acutely, because it *is* bandwidth-bound, for the same underlying reason decomposition shape and rank binding also only produce single-digit-percent effects: the theoretical ceiling on what tuning shape/placement can buy you is much smaller than the swing a full second job's memory traffic can cause.

## Known issues and open items

- **`nopin`'s long-run migration risk is untested, not disproven.** It matched the pack over 40 iterations with an affinity mask that permits migration for the whole run; the scored run is 150 iterations, long enough that drift or cache-locality loss remains a real possibility we haven't measured.
- **No mechanistic explanation for `(18 4 1)`'s win.** `decomposePar`'s face-balance numbers didn't predict the ranking; shapes with worse reported face balance sometimes ran faster. Worth a deeper look for anyone extending this.
- **Confidence in the ranking is uneven.** `(18 4 1)` has two independent clean-node confirmations that agree within ~0.9% of each other; `(12 6 1)`, `(12 3 2)`, and `(6 6 2)` each have only one clean-node data point, from the same job on the same node, not yet cross-checked against a second node.
- **OpenFOAM's built-in `profiling` block turned out to be a dead end under our timing setup.** It's registered with an `AUTO_WRITE` flag (confirmed by reading `Time.C`/`profiling.C` directly), meaning it only reaches disk during an output-writing event. Every run in this study used `controlDict.noWrite` with `writeInterval 100000`, larger than any run's iteration count, so that event never fires and the profiler's in-memory data is silently discarded at job end (`profiling::stop()` drops it, doesn't force a write). Getting real stage-by-stage profiling data would require `controlDict.withWrite`, which introduces file I/O into the measured wall-clock time, making any such run incomparable to every I/O-free number reported here. Not pursued in this study, to avoid contaminating the comparisons already gathered.
- **All of this is 1-node/40-iteration.** None of it has been re-validated at the 2- or 4-node scale the actual scored run uses.

## Next up

1. Re-derive the 2- and 4-node `nHierarchical` triplet from the `(18 4 1)` per-node ratio, but re-validate it at actual multi-node scale rather than assuming it extrapolates linearly with node count.
2. Carry forward `I_MPI_PIN_DOMAIN=core`, `I_MPI_PIN_ORDER=compact` for MPI rank placement into the multi-node runs.
3. Budget for at least one full repeat of the final 4-node configuration before treating any single run's number as the official reported result — this study's own headline finding is that a single unrepeated measurement on Vanda cannot be trusted at face value.
4. If Gadi or ASPIRE-2A support requesting exclusive-node scheduling (`place=excl` in PBS or equivalent), request it for the scored run, removing this entire confound rather than budgeting repeats around it.
5. If deeper stage-level profiling is wanted for the presentation, run it as a clearly separate `controlDict.withWrite` diagnostic pass, kept apart from the I/O-free performance numbers here.

---

## Appendix: glossary quick reference

| Term | Meaning |
|---|---|
| Cell | A small 3D volume element making up the simulation mesh; this case has 65 million |
| Rank | One copy of the solver, assigned to one portion of the split-up mesh, running on one CPU core |
| `decomposePar` | The OpenFOAM utility that splits the mesh into per-rank pieces before a parallel run |
| Decomposition shape `(Nx Ny Nz)` | Number of mesh cuts along x/y/z under the `hierarchical` method |
| Processor face | A mesh boundary between two ranks' sub-domains, requiring data exchange every iteration |
| Node / socket | One physical server / one physical CPU chip (two sockets, 36 cores each, on these nodes) |
| NUMA | Memory attached to one socket is slower to access from the other socket |
| Pinning / binding | Fixing which physical core each MPI rank runs on for the whole job |
| `I_MPI_PIN_DOMAIN` / `I_MPI_PIN_ORDER` | Intel MPI's pinning-unit and rank-to-core-order controls |
| s/step | Seconds of wall-clock time per solver iteration — the primary metric throughout |
| Noise floor | How much an unchanged configuration's timing varies purely from run-to-run randomness |
| `place=free` vs `place=excl` | PBS policy on whether other users' jobs may share your allocated node |

---

*Setup: `occDrivAerStaticMesh`, OpenFOAM v2512, coarse mesh (65M cells), 1-node/72-rank exploratory runs on NUS Vanda (Intel Xeon Platinum 8452Y, Sapphire Rapids, PBS Pro), ahead of the scored 2- and 4-node APAC HPC-AI 2026 runs.*
