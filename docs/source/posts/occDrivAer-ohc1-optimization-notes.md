---
title: "Optimizing OpenFOAM's occDrivAer Case for the APAC HPC-AI Competition 2026"
description: "Notes on the APAC HPC-AI 2026 Competition's OpenFOAM task, the OHC-1 benchmark it's based on, and what we learned about decomposition, renumbering, compiler flags, and MPI tuning for the occDrivAerStaticMesh case."
date: 2026-09-25
tags: [hpc, openfoam, cfd, decomposition, mpi]
---

# Optimizing OpenFOAM's occDrivAer Case for the APAC HPC-AI Competition

*Working notes from preparing the OpenFOAM HPC task for the APAC HPC-AI 2026 Competition. This post covers the competition itself, the OHC-1 benchmark the task is derived from, the physical structure of the occDrivAer case, and the decomposition / renumbering / compiler / MPI settings we identified as worth testing.*

---

## 1. What the APAC HPC-AI Competition is

The **APAC HPC-AI Competition** is an annual student competition jointly organized by the **HPC-AI Advisory Council**. It is open to university and technical-institute teams from across the Asia-Pacific region and pairs two disciplines in one event: high-performance computing and artificial intelligence. Teams tackle both workloads in parallel across the competition period, then presenting their optimization work to judges. Teams get hands-on access to real national-scale supercomputing resources (historically including NSCC Singapore's systems and NCI's Gadi) to develop and benchmark their optimizations.

In the edition these notes are drawn from, the two tasks are:
- An **AI task** built around the Qwen model family.
- An **HPC task** built around **OpenFOAM**, specifically a CPU-optimization challenge using the `occDrivAerStaticMesh` case (detailed below).

Each team gets a single interview covering both tasks. Judges award two separate presentation scores (60% of each task's grade), with the remaining 40% of the HPC score coming from the measured 4-node performance metric. Teams choose between NCI **Gadi** or NSCC **ASPIRE-2A** as their scored supercomputer; a practice cluster (**Vanda**, Sapphire Rapids, PBS Pro) is used for iteration and debugging before spending limited allocation hours on the real scored systems.

*Sources: HPC-AI Advisory Council / NSCC / NCI competition announcements (2018–2026); local task rules document for this competition edition.*

---

## 2. What OHC-1 is

The OpenFOAM task is derived from the **OpenFOAM HPC Challenge (OHC-1)**, the first community-run HPC benchmarking exercise organized by the OpenFOAM HPC Technical Committee (HPCTC), culminating in a mini-symposium at the 20th OpenFOAM Workshop in Vienna (July 2025).

**Scale of OHC-1:** 12 contributing organizations (academia and industry, Wikki GmbH, Huawei, CINECA, University College Dublin, Universität der Bundeswehr München, BAW, University of Minho, TU Munich, UKAEA, Engys, E4 Computer Engineering, CFD FEA Service) submitted **237 valid data points**: 175 in a **hardware track** and 62 in a **software track**. Runs spanned single-node configurations up to 256 nodes (32,768 CPU cores), across 25 distinct CPU models (AMD, Intel, ARM), with wall-clock times ranging from 7.8 minutes to 65.7 hours and reported energy consumption from 2.1 to 236.9 kWh per run.

**Headline findings from the OHC-1 paper:**
- A **Pareto front** between time-to-solution and energy-to-solution exists; pushing for lower wall-clock time past a point yields diminishing returns at sharply higher energy cost.
- **Single-node performance is memory-bandwidth-bound.** CPUs with on-package high-bandwidth memory (HBM) dominated single-node results, consistent with OpenFOAM's memory-bound sparse linear-algebra kernels.
- **Multi-node performance is communication-bound.** Because OpenFOAM parallelizes exclusively via MPI, a practical strong-scaling limit of roughly **10,000 cells per core** was observed across submissions, below that, communication cost exceeds computational work.
- **Software-track optimizations meaningfully beat hardware-track baselines**: up to 28% lower energy per iteration, 17% higher FVOPS (finite-volume operations per second) per node, and up to 72% faster single-timestep wall-clock time, achieved through full GPU ports, linear-solver GPU offloading, decomposition optimization, mixed precision, selective memory allocation, and coherent parallel I/O.
- Reported core counts in the analysis were corrected to **physical cores**, hyperthreads were explicitly disregarded when computing scaling metrics.

*Source: Lesnik, Olenik & Wasserman, "The First OpenFOAM® HPC Challenge (OHC-1)," 2026 (arXiv:2603.27565). Data/spreadsheets: [github.com/OpenFOAM-HPC-Challenge/OHC1](https://github.com/OpenFOAM-HPC-Challenge/OHC1). Case repository: [develop.openfoam.com/committees/hpc](https://develop.openfoam.com/committees/hpc).*

---

## 3. The occDrivAer case itself

### 3.1 Geometry

**occDrivAer** = **o**pen-**c**losed **c**ooling **DrivAer**. It's the notchback variant of the Ford Open Cooling DrivAer (OCDA), a generic but industrially realistic full car body with a complex underbody and engine-bay cooling channel geometry, previously used as a benchmark case in the AutoCFD2/3/4 workshops. For this challenge the cooling inlets are sealed shut and the wheels are static (no rotation), simplifications that make it a clean, repeatable HPC benchmark rather than a full aerodynamic validation exercise.

### 3.2 Flow conditions and domain

| Parameter | Value |
|---|---|
| Fluid | Air, ν = 1.507 × 10⁻⁵ m²/s |
| Inlet velocity | 38.889 m/s (140 km/h) |
| Wheelbase (L_ref) | 2.78618 m |
| Reynolds number | ≈ 7.19 × 10⁶ |
| Domain (upstream / downstream) | 40 m / 80 m from front axle |
| Domain width | 44 m (±22 m) |
| Domain height | 20 m; floor at −0.3176 m |
| Turbulence model | k-ω SST |
| Solver | `simpleFoam` (steady-state incompressible RANS, SIMPLE algorithm, fixed inner iterations) |

### 3.3 Mesh

Generated with `snappyHexMesh` from a `blockMesh` background at cell level L0 = 1 m, refined through ~9 levels to a surface resolution of ~1.95 mm (finest feature refinement ~0.96 mm). Two prism layers on the wall (e.g. 0.8 mm wall-normal on the roof), targeting **wall functions** (y⁺ > 30 over most of the surface) rather than a wall-resolved mesh.

Refinement is structured as **nested/concentric boxes** around the car, densest at the surface, underbody/engine-bay channels, and wake region; coarsening quickly back to background resolution in the far-field. Three pre-generated resolutions exist (same procedure, different starting background resolution):

| Mesh | Cells |
|---|---|
| Coarse | 65M |
| Medium | 110M |
| Fine | 236M |

This competition's scored task uses the **65M coarse mesh**, unmodified.

### 3.4 Expected behavior / sanity check

Reference (fully converged, fine-mesh) force coefficients from the OHC-1 paper: **Cd = 0.262, Cl = 0.0787, Cs = 0.0116**. On the coarse mesh at low iteration counts (this competition's 40/80/150-iteration scaling runs), Cd is still transient and converges *toward* that reference, official sanity-check values are Cd ≈ 0.43 at 40 iterations, ≈ 0.34 at 80, and ≈ 0.28–0.29 at 150. A result far outside this range indicates a broken run, not just an under-converged one.

---

## 4. Decomposition methods, what they are and how they differ

`decomposePar` decides **which MPI rank owns each cell**. The method controls processor-boundary size (communication cost) and load balance.

| Method | Basis | Load balance | Comm. minimization | Tunable to hardware | Decompose cost | Extra library needed |
|---|---|---|---|---|---|---|
| **hierarchical** | Geometric bisection (slab cuts along x/y/z, in order) | Good on fairly regular meshes | Not directly optimized | **Yes**, explicit `n (nx ny nz)` | Very low | No |
| **scotch** | Graph partitioning (multilevel, minimizes cut edges) | Good, self-balancing | Yes | No, shape not controllable | Moderate | No (bundled) |
| **metis** | Graph partitioning (Karypis & Kumar) | Good | Yes | No | Moderate | Yes (ThirdParty) |
| **kahip** | Graph partitioning (typically highest quality) | Best | Best | No | Highest | Yes (ThirdParty, needs `cmake`) |

**Why `hierarchical` works well for this specific case:** occDrivAer's refinement is a set of nested, axis-aligned boxes around a compact car-shaped region inside a much larger, mostly-uniform far-field, a shape geometric bisection handles reasonably evenly. Just as importantly, `hierarchical` is the *only* method where the decomposition shape can be deliberately aligned to node/socket/core hardware topology, rather than accepting whatever a graph partitioner produces.

**Caveat discovered:** hierarchical balances by **cell count**, not face count. Because the dense car/wake region is geometrically thin, cuts through it produce disproportionately more processor-boundary faces per cell than cuts through the empty far-field, this can be invisible if only per-rank *cell* counts are checked in `decomposePar` logs. Worth checking face-count balance too:

```bash
grep -A 30 "Processor" logFiles/10_decomposePar.log | grep -i "faces\|cells"
```

---

## 5. Renumbering, what RCM means

Decomposition decides *which rank* owns a cell; **renumbering decides the in-memory ordering of cells within a rank**. They solve different problems: decomposition minimizes inter-rank communication, renumbering minimizes cache misses during computation on each rank.

**RCM = Reverse Cuthill-McKee.**

1. Treat the (per-rank) mesh as a graph, cells as nodes, shared faces as edges.
2. **Cuthill-McKee**: breadth-first traversal from a low-degree starting node, assigning indices in visitation order, so geometrically adjacent cells get numerically close indices.
3. **Reverse**: simply reversing the resulting index order empirically improves numerical/fill-in behavior for iterative solvers, at no extra cost.

**Effect:** collapses the sparse matrix's nonzero pattern into a narrow band around the diagonal, neighboring cells become neighboring memory addresses, sharply reducing cache misses on every matrix-vector operation, every iteration, with **zero change to the underlying math or result**.

**Why it matters more here than usual:** this case is memory-bandwidth-bound (Section 2), so a technique that improves *reuse* of the bytes already moved from RAM is exactly the right lever, even though it doesn't reduce total bytes moved.

**Already in the pipeline correctly:**
```bash
renumberMesh -constant -overwrite -parallel
```
RCM is `renumberMesh`'s **default**, no flag needed. Order matters: renumbering runs *after* decomposition (`decomposePar → restore0Dir → renumberMesh -parallel`), since each rank only needs its own local subdomain's ordering optimized, which is a separate, smaller graph than the full mesh.

Confirm it's doing real work:
```bash
grep -i "renumber\|bandwidth" logFiles/20_renumberMesh.log
```

---

## 6. What every top OHC-1 hardware-track submission actually used

We pulled the OHC-1 submission spreadsheets directly (Huawei, Wikki, UniBwM, BAW, the four teams whose 65M-coarse-mesh hardware-track results are cited as the sanity-check reference for this competition) and read their `Simulations` sheets for the 4-node configuration:

| Team | Hardware | Nodes | Cores | Decomp. method | Renumber | s/iteration |
|---|---|---|---|---|---|---|
| Huawei | LX2 (Huawei ARM CPU) | 4 | 1024 | `hierarchical` | `RCM` | 1.247 |
| BAW | AMD EPYC 9654 | 4 | 768 | `hierarchical` | `RCM` | 1.425 |
| Wikki | AMD EPYC 7763 | 4 | 512 | `hierarchical` | `RCM` | 3.467 |
| Wikki | Intel Xeon 8480+ | 4 | 448 | `hierarchical` | `RCM` | 2.520 |
| UniBwM | AMD EPYC 7662 | 4 | 512 | "standard"* | "standard"* | 6.817 |

\* Almost certainly means "kept the case-provided default", i.e. also hierarchical/RCM, not a genuinely different method.

**Every team that specified a method used the same combo: `hierarchical` decomposition + `RCM` renumbering.** Nobody switched to `scotch`/`kahip` to win their scored run. Caveats: all four ran **OpenFOAM v2412** (this competition requires v2512) and used **2000 iterations** (not this competition's 40/80/150 scaling scheme), so this validates *method choice*, not raw performance targets.

*Sources: OHC-1 submission spreadsheets, `Simulations` sheet, rows ~15–26, `05_Huawei_OHC1_DrivAer_Result_Hardware_Coarse.xlsm`, `01_Wikki_OHC1_DrivAer_Result_hardware_65M.xlsm`, `06_OHC1_DrivAer_Result_UniBwM_EPYC_Coarse_Scaling.xlsm`, `07_OHC1_DrivAer_coarse_mesh_Schulze_BAW.xlsm`, all at [github.com/OpenFOAM-HPC-Challenge/OHC1/tree/main/submissions](https://github.com/OpenFOAM-HPC-Challenge/OHC1/tree/main/submissions).*

---

## 7. Rank count, the cells/core sweet spot

Using OHC-1's ~10,000 cells/core practical floor (Section 2) against the fixed 65M-cell coarse mesh:

| Nodes | ~128 cores/node (e.g. Aspire2A) | Cells/core |
|---|---|---|
| 1 | 128 | ~508,000 |
| 2 | 256 | ~254,000 |
| 4 | 512 | ~127,000 |

All comfortably inside the "good" zone (100k–1M cells/core), cells/core is not the binding constraint at 4 nodes on this mesh, so there's headroom before communication overhead dominates.

**SMT / hyperthreading:** OHC-1's own analysis discounted hyperthreads, counting only physical cores when computing scaling metrics, consistent with a bandwidth-bound workload where filling every hardware thread adds shared-bus contention without adding memory channels. Rank count should track physical cores by default; treat "fill every thread" as an experiment to run and measure, not an assumption.

---

## 8. Settings to try, summary checklist

In priority order (cheapest / highest-leverage first):

### 8.1 Face-balance check (do first, free)
```bash
grep -A 30 "Processor" logFiles/10_decomposePar.log | grep -i "faces\|cells"
```
Confirms whether the car/wake-region face imbalance (Section 4) is actually present before spending time re-tuning.

### 8.2 Re-derive `nHierarchical` from real topology
Put the **coarsest split on the long flow axis (x)**, matching node count; finer splits (socket, then core) on y/z:

```
// system/include/caseDefinition
nCores              <total physical cores across N nodes>;
nHierarchical       (<nodes-axis> <socket-axis> <core-axis>);
```
```
// system/decomposeParDict
method              hierarchical;
hierarchicalCoeffs
{
    n           ($nHierarchical);
    delta       0.001;     // try 0.01 if boundary artifacts appear, given the boxed refinement
    order       xyz;
}
```

### 8.3 Physical cores vs. full SMT, test, don't assume
```bash
# Physical-core run
#PBS -l select=4:ncpus=<physical_cores_per_node>:mpiprocs=<physical_cores_per_node>:ompthreads=1

# Full-SMT run
#PBS -l select=4:ncpus=<logical_threads_per_node>:mpiprocs=<logical_threads_per_node>:ompthreads=1
```
Compare `Average wall-clock time per time step` between the two directly.

### 8.4 Compiler flags (secondary, bandwidth-bound workload, smaller return than decomposition)
```bash
# Sapphire Rapids (Vanda / Gadi normalsr)
export CFLAGS="-O3 -march=sapphirerapids -mtune=sapphirerapids"
export CXXFLAGS="-O3 -march=sapphirerapids -mtune=sapphirerapids"

# Zen3 Milan (Aspire2A-class)
export CFLAGS="-O3 -march=znver3 -mtune=znver3"
export CXXFLAGS="-O3 -march=znver3 -mtune=znver3"
```
Build only on a **compute node** (interactive job), never a login node, login nodes can run an emulated/different microarchitecture from compute nodes.

### 8.5 MPI rank binding, matches the `nHierarchical` layout
```bash
mpirun -np ${nProcs} \
  --bind-to core \
  --map-by numa \
  ${OMPI_FLAGS} \
  simpleFoam -parallel
```
Keep regardless of target (fixes a confirmed vader/CMA log-flood + OOM issue):
```bash
export OMPI_MCA_btl_vader_single_copy_mechanism=none
```
Worth A/B testing once running multi-node (currently commented out in the template `Allrun`):
```bash
OMPI_FLAGS="--mca pml ucx"
```

### 8.6 Confirm RCM renumbering is doing real work
```bash
grep -i "renumber\|bandwidth" logFiles/20_renumberMesh.log
```

---

## 9. Key takeaways

1. **Decomposition method and renumbering method are already correct.** `hierarchical` + `RCM` match what every top OHC-1 hardware-track submission used, there's no method to switch to, only numbers to tune.
2. **The mesh's non-uniform refinement (nested boxes around the car/wake) means cell-count balance ≠ face-count balance.** Check both before concluding a decomposition is "good."
3. **This workload is memory-bandwidth-bound, not compute-bound**, this is why decomposition/renumbering/rank-placement outweigh compiler vectorization flags, and why RCM (a cache-reuse optimization) pays off specifically here.
4. **~10,000 cells/core is the practical floor**; the 65M coarse mesh at 4 nodes sits well within the efficient range regardless of target cluster.
5. **Physical-core rank counts are the safer default** given the bandwidth-bound nature of the workload, SMT oversubscription should be tested, not assumed.
6. **Validate cheaply on a practice cluster first** (e.g. Vanda), none of the method/tuning changes here touch mesh, solver, or physics, so they're exactly what's safe to iterate on before spending limited scored-cluster hours.

---

## References

- Lesnik, S., Olenik, G., Wasserman, M., *The First OpenFOAM® HPC Challenge (OHC-1)*, 2026. [arXiv:2603.27565](https://arxiv.org/html/2603.27565v1)
- OHC-1 case repository, [develop.openfoam.com/committees/hpc](https://develop.openfoam.com/committees/hpc/-/tree/develop/incompressible/simpleFoam/occDrivAerStaticMesh)
- OHC-1 submission data & analysis notebooks, [github.com/OpenFOAM-HPC-Challenge/OHC1](https://github.com/OpenFOAM-HPC-Challenge/OHC1)
- 20th OpenFOAM Workshop, Vienna, 2025, Book of Abstracts (Zenodo, DOI: 10.5281/zenodo.18670150)
- HPC-AI Advisory Council / NSCC Singapore / NCI Australia, APAC HPC-AI Competition (annual, since 2018)
