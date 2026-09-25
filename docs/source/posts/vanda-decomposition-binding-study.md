---
title: "occDrivAerStaticMesh on Vanda: A 1-Node Decomposition and MPI-Binding Study"
date: 2026-09-25
tags: [openfoam, hpc, vanda, pbs, decomposition, mpi]
---

# occDrivAerStaticMesh on Vanda: A 1-Node Decomposition and MPI-Binding Study

**Case:** occDrivAerStaticMesh (OpenFOAM HPC Challenge, OHC-1), 65M-cell coarse mesh
**Cluster:** NUS Vanda (PBS Pro), Intel Xeon Platinum 8452Y (Sapphire Rapids), 72 physical cores / 512 GB per node
**Build:** OpenFOAM v2512 (openfoam.com), Intel compilers 2024.2.0, Intel MPI 2021.13.0
**Goal:** identify the best single-node mesh-decomposition shape and MPI rank-binding setting before committing walltime to the scored 2- and 4-node runs on Vanda / Gadi / ASPIRE-2A.

This write-up documents the full investigation, including the dead ends and a shared-cluster contention artifact that turned out to be a bigger factor than anything we deliberately tuned. It is written to be self-contained: every technical term is defined the first time it is used, so no prior HPC or OpenFOAM background is assumed.

---

## 0. Background: what problem is being solved, and what the vocabulary means

### 0.1 What OpenFOAM and this case are

**OpenFOAM** is an open-source software package for Computational Fluid Dynamics (CFD), simulating how fluids (air, water, etc.) move, using the Navier–Stokes equations solved numerically on a computer. A simulation is called a **case**, defined by a 3D geometry, a mesh (see below), physical parameters, and solver settings.

**occDrivAerStaticMesh** is a specific, standardized case: airflow around a realistic car body (the "DrivAer" generic vehicle shape used across the automotive-CFD research community) at highway speed (140 km/h), with the wheels held static (not rotating) and the mesh fixed (not adapting during the run). It is the reference workload for the **OpenFOAM HPC Challenge (OHC-1)**, a competition benchmark used to compare how efficiently different teams/clusters can run the same simulation.

**simpleFoam** is the specific OpenFOAM *solver* (the program that actually performs the iterative numerical calculation) used for this case. It solves the steady-state, incompressible form of the flow equations using an algorithm called SIMPLE (Semi-Implicit Method for Pressure-Linked Equations). "Steady-state" means the solver is not simulating time evolving forward in real seconds; instead it performs a sequence of numerical **iterations** (sometimes loosely called "steps" in the logs) that converge toward a final, unchanging flow solution. When this document refers to "iterations" or "time steps," it means these solver iterations, not physical simulation time.

**Mesh / cells:** the 3D volume around the car is broken into millions of small volume elements called **cells**, this case uses a 65-million-cell mesh (the "coarse" resolution option; finer meshes with more cells also exist for this case but are not used here). Each cell holds numerical values (velocity, pressure, etc.) that get updated every iteration based on its neighboring cells.

### 0.2 Why the mesh needs to be split up: parallel computing basics

Running 65 million cells' worth of calculation on a single CPU core would take an impractically long time. **HPC (High-Performance Computing)** clusters solve this by splitting the work across many **CPU cores** running simultaneously, this is called **parallel computing**.

- A **CPU core** is one independent processing unit capable of running one stream of instructions at a time. A modern server typically has many cores on a single physical chip; the machines in this study have 72 cores per node (see §0.4).
- **MPI (Message Passing Interface)** is the standard software protocol used to run a program across many cores (and potentially many separate physical machines) at once, where each copy of the program, called a **rank**, works on its own portion of the problem and periodically sends data to other ranks over the network or shared memory. In this case, MPI is used to split the 65M-cell mesh into 72 pieces, one per CPU core, all running simpleFoam simultaneously and exchanging data at cell boundaries every iteration.
- **decomposePar** is the OpenFOAM utility that performs this split, it partitions the full mesh into a number of smaller sub-meshes (one per intended MPI rank), each written to its own `processorN` directory (`processor0`, `processor1`, ... `processor71` for a 72-way split). This process is called **domain decomposition**.
- Cells that sit at the boundary between two sub-meshes require the two ranks that own them to exchange information every iteration, these boundary connections are called **processor faces**, and their count is a rough proxy for how much communication overhead a given decomposition will incur (more processor faces generally means more data has to be exchanged per iteration, which costs time).

### 0.3 How the mesh gets split: decomposition methods and shapes

OpenFOAM offers several **decomposition methods** (algorithms for deciding which cells go to which rank):

- **`hierarchical`**: splits the mesh along the x, y, and z spatial axes in a fixed number of cuts per axis, specified as a triplet `(Nx Ny Nz)`, e.g. `(18 4 1)` means 18 cuts along x, 4 along y, and 1 (no cut) along z, giving 18 × 4 × 1 = 72 total sub-domains. This method is fully deterministic: the same triplet on the same mesh always produces exactly the same split, every time. In this document, "decomposition shape" always refers to this `(Nx Ny Nz)` triplet.
- **`scotch`**: a graph-based partitioning algorithm that analyzes the mesh's connectivity and tries to produce a more communication-efficient split than a simple geometric cut, at the cost of being non-deterministic (small run-to-run randomness in the partitioning) unless a fixed random seed is explicitly set.
- **`multiLevel`**: a hybrid method used elsewhere in this project's 4-node configuration, combining a `hierarchical` split across physical nodes with a `scotch` split within each node.

This study uses `hierarchical` exclusively for its timing comparisons, specifically because its determinism means a competition judge can rerun the exact same job and get an identical mesh split, a reproducibility property `scotch` cannot guarantee without extra seeding.

**Total rank count** must always equal the total core count being used in a given run, e.g. an `(18 4 1)` shape multiplies to 72, matching this study's 72-core single-node runs.

### 0.4 The hardware: cores, sockets, and NUMA

- Each compute node used in this study has **72 physical CPU cores**, arranged as **two CPU chips ("sockets")** on the motherboard, each socket containing 36 cores.
- **NUMA (Non-Uniform Memory Access)** describes a hardware property of multi-socket servers: each socket has its own bank of directly-attached memory (RAM), and while any core can access any memory location, accessing memory attached to the *other* socket ("cross-socket" or "cross-NUMA" access) is slower than accessing memory on its own socket. This matters for MPI placement (§0.5): if two ranks that talk to each other constantly end up on different sockets, every exchange between them pays this cross-socket latency penalty.
- The Xeon Platinum 8452Y (the specific CPU model in these nodes, from Intel's "Sapphire Rapids" generation) does not use simultaneous multithreading in this configuration, each of the 72 cores runs exactly one MPI rank in every experiment in this study (i.e., 72 ranks on 72 cores, no oversubscription).

### 0.5 MPI rank placement / "pinning"

**CPU pinning (or "binding")** is the practice of explicitly telling the operating system which physical core each MPI rank must run on for the duration of the program, rather than letting the OS scheduler decide freely. Pinning matters because:
1. It prevents the OS from migrating a rank to a different core mid-run, which can hurt CPU cache performance (a rank that stays on one core keeps reusing data already loaded into that core's fast local cache memory).
2. It lets you deliberately control which ranks end up sharing a socket (and therefore have fast, low-latency communication with each other) versus which ranks are split across sockets (slower, cross-NUMA communication).

This study uses **Intel MPI** (the specific MPI software implementation installed on Vanda), whose pinning behavior is controlled by two environment variables:
- **`I_MPI_PIN_DOMAIN`**: sets the *unit* of pinning. `core` means "one MPI rank per physical core" (as opposed to, e.g., letting a rank roam across multiple cores).
- **`I_MPI_PIN_ORDER`**: sets the *order* in which rank numbers (rank 0, rank 1, rank 2, ...) get assigned to core numbers. This is the specific setting swept in §4 below, with options including `compact`, `scatter`, `bunch`, `spread`, and disabling pinning entirely.

Important distinction for anyone cross-referencing other HPC documentation: **OpenMPI** (a different, commonly-used MPI implementation) uses entirely different flags for the same concept (`--bind-to`, `--map-by`). Vanda's PBS job template for this case uses Intel MPI, so `I_MPI_PIN_*` variables are the correct and only relevant controls here, OpenMPI's flags would not work.

### 0.6 The measurement: what "s/step" means and how it's obtained

simpleFoam's log output prints, after each solver run completes, a line reading `Average wall-clock time per time step = X`, where X is in seconds. This is computed by the solver itself, averaging the real (wall-clock, i.e. actual elapsed) time taken per iteration across the run (excluding the very first iteration, which includes one-time setup overhead). This is the **primary performance metric** used throughout this study and in the underlying competition, lower is better, and it is what "s/step" refers to in every table below.

### 0.7 The scheduler: PBS Pro, jobs, and nodes

Vanda is a shared, multi-user cluster. Users do not run programs directly on the machines; instead they submit **jobs**, a script describing what to run and what resources (CPU cores, memory, time limit) it needs, to a **scheduler**, which queues jobs and assigns them to available physical machines (**nodes**) when resources free up. Vanda's scheduler is **PBS Pro**, controlled via the `qsub` (submit a job), `qstat` (check job status), and `pbsnodes` (inspect a node's hardware/occupancy) commands. Each node has a hostname such as `CN-099` or `GN-A40-078` (the latter being a node that also has a GPU installed, though this study used only its CPUs).

A PBS request such as `select=1:ncpus=72:mpiprocs=72:mem=500gb` asks for 1 node, 72 CPU cores, 72 MPI processes, and 500 GB of memory. Critically for §3 below: by default (`place=free`), PBS does **not** guarantee that a job gets a node entirely to itself, other users' jobs can be scheduled onto the same physical node simultaneously, sharing its remaining resources, unless exclusive access is explicitly requested and granted.

---

## 1. Setup

- Working directory: `/scratch/$USER/hpc-committee-test/incompressible/simpleFoam/occDrivAerStaticMesh_vanda_decomptest`
- Pipeline followed the competition's mandated Allrun sequence exactly: `decomposePar -constant` → `restore0Dir -processor` → `renumberMesh -constant -overwrite -parallel` → `potentialFoam -initialiseUBCs -parallel` → `applyBoundaryLayer -ybl 0.0450244 -parallel` → `simpleFoam -parallel`. (`renumberMesh` reorders cell numbering for better memory-access locality; `potentialFoam` and `applyBoundaryLayer` compute a fast approximate starting flow field so the main solver converges faster than starting from a blank/zero field; none of these steps may be skipped or altered under the competition rules.)
- `fvSolution.fixedIter` (the "hardware track" solver-tolerance settings, fixed number of inner iterations per outer step, for consistent per-step timing) and `controlDict.noWrite` (a settings file that disables writing output data to disk during the run, so the measured time reflects solver computation only, not file I/O) were used for every timing run in this study.
- All single-node experiments ran at 72 ranks (`nCores 72`), 40 iterations (`endTime 40`), matching the competition's official 1-node scaling rule (the competition specifies 40 iterations at 1 node, 80 at 2 nodes, 150 at 4 nodes, so that later-stage results are comparable across node counts).
- `decompositionMethod hierarchical` was used throughout instead of `scotch`, see §0.3 for the reproducibility reasoning.

---

## 2. Decomposition shape sweep

### 2.1 Initial sweep (later found to be on a contended node)

The first sweep tested 8 decomposition shapes, all at `nCores 72`, submitted as a single PBS job so all 8 ran back-to-back on the same physical node (later identified as **CN-099**):

| Shape `(Nx Ny Nz)` | Pin order | s / step |
|---|---|---:|
| `(12 6 1)` | default (no explicit pin) | 17.874 |
| `(12 6 1)` | compact | 17.678 |
| `(12 6 1)` | scatter | 17.679 |
| `(24 3 1)` | compact | 17.765 |
| `(36 2 1)` | compact | 17.788 |
| `(18 4 1)` | compact | 17.411 |
| `(12 3 2)` | compact | **17.272** |
| `(6 6 2)` | compact | 17.507 |

At face value, `(12 3 2)`, splitting into 12 pieces along x, 3 along y, and additionally 2 along z (the only shape in this batch to cut the vertical axis at all), looked like the fastest. This result did **not** survive re-testing on clean (uncontended) nodes, as shown next.

### 2.2 Re-verification on clean nodes

Once node-to-node contention was identified as a confound (full explanation in §3), the leading shapes were re-run on nodes subsequently confirmed to be free of interference from other users' jobs.

Two independent runs of `(18 4 1)`, on two different physical nodes:

| Shape | Node | s / step |
|---|---|---:|
| `(18 4 1)` | CN-090 | 9.176 |
| `(18 4 1)` | CN-108 | 9.095 |

Three other shapes, all run back-to-back within a single PBS job on one node (`GN-A40-078`, a GPU-equipped node used here purely for its CPUs, PBS scheduled a CPU-only request onto it):

| Shape | Node | s / step |
|---|---|---:|
| `(12 6 1)` | GN-A40-078 | 9.599 |
| `(12 3 2)` | GN-A40-078 | 9.602 |
| `(6 6 2)` | GN-A40-078 | 9.735 |

**Finding:** on clean nodes, `(18 4 1)` is consistently fastest, confirmed independently on two separate nodes at roughly 9.1–9.2 s/step, about 4.5–6.5% faster than the other three shapes tested. `(12 3 2)`'s apparent lead in the original CN-099 sweep is attributed to the contention artifact described in §3, which inflated all eight of that sweep's timings by a similar factor, preserving *some* relative ordering by chance, but not reliably, since the true ranking flipped once contention was removed.

**Honest caveat:** `(18 4 1)` has two independent clean-node confirmations that agree closely (9.176 and 9.095, within about 0.9% of each other). `(12 6 1)`, `(12 3 2)`, and `(6 6 2)` each have only a single clean-node data point, and all three came from the same job on the same node, so they have not been cross-checked against a second, independent node the way `(18 4 1)` has. Given the walltime budget available for this exploratory phase, this level of confidence was judged acceptable to proceed on, but it is not exhaustive.

### 2.3 Selected configuration

```
nCores              72;
decompositionMethod hierarchical;
nHierarchical       (18 4 1);
```

No mechanistic explanation for *why* `(18 4 1)` performs best was established during this study, the processor-face-count balance reported by `decomposePar` (see §0.2) did not cleanly predict the ranking across the shapes tested; shapes with objectively worse face-balance sometimes ran faster than shapes with better balance. This is reported here as an empirical finding, not a theoretically derived one, and is flagged as an open question for anyone extending this work.

---

## 3. Discovery: node-to-node contention on a shared cluster

### 3.1 The anomaly

To check how much a single configuration's timing varies from run to run purely due to system noise (a "**noise floor**", see the plain-language explanation below), the `(12 3 2)` configuration (72 ranks, `compact` pinning) was resubmitted as an identical repeat. It happened to land on a different physical node than the original sweep, and came back **47% faster**:

| Run | Node | s / step |
|---|---|---:|
| Original sweep | CN-099 | 17.272 |
| Repeat 1 | CN-142 | 9.188 |
| Repeat 2 | CN-142 | 9.241 |
| Repeat 3 | CN-051 | 9.256 |
| Repeat 4 | CN-051 | 9.167 |

*(Plain-language aside on "noise floor": if you weigh yourself twice in a row on the same scale without doing anything different in between, you might get two slightly different numbers just from measurement noise, not because your weight actually changed. The "noise floor" here is the equivalent idea: how much does the exact same OpenFOAM configuration vary in timing, run to run, with nothing intentionally changed? If a difference you're investigating, like which decomposition shape is faster, is smaller than this noise floor, you can't trust it as a real effect.)*

Four repeat runs across two different, independently-selected nodes clustered tightly together, 9.167 to 9.256 s/step, under a 1% spread. This is a normal, healthy noise floor. The original CN-099 result sat entirely outside that band, at roughly **1.9× slower** than the cluster of four clean repeats.

### 3.2 Diagnosis

- `pbsnodes` (the PBS command that reports a node's hardware specs and current job occupancy) reported **identical** resource specifications for CN-099 and the clean nodes, same 72 `ncpus`, same memory, same CPU architecture string. Nothing distinguished them as different hardware tiers.
- A stage-by-stage timing comparison isolated the slowdown specifically to the main `simpleFoam` solve, not the pipeline's shorter preparation steps:

| Stage | CN-099 | CN-142 | Ratio |
|---|---:|---:|---:|
| renumberMesh | 3.72 s | 4.20 s | ~1.1× |
| potentialFoam | 31.59 s | 30.83 s | ~1.0× |
| applyBoundaryLayer | 5.26 s | 5.37 s | ~1.0× |
| **simpleFoam (40 steps, avg/step)** | **17.27 s** | **9.19 s** | **~1.9×** |

The three short utility stages agreed to within roughly 10% on both nodes. Only the long, sustained `simpleFoam` solve, which runs for 12+ minutes and is known to be limited primarily by how fast data can be moved between CPU and memory ("**memory bandwidth-bound**," meaning the CPU spends more time waiting on memory transfers than on raw arithmetic), showed the large gap. This pattern (short stages unaffected, long sustained stage badly affected) is exactly what would be expected from another job competing for the same node's shared memory bandwidth, rather than from a genuine hardware or clock-speed difference between the two nodes (a real hardware difference would be expected to slow down every stage roughly proportionally, not just one).
- `pbsnodes CN-099` and `pbsnodes CN-142`, checked at the time these jobs were running, both showed **other users' array jobs actively co-resident** on the same physical node. PBS's default node-sharing policy (`place=free`, as opposed to `place=excl` for exclusive access) permits this: requesting `select=1:ncpus=72:mem=500gb` reserves that specific amount of CPU and memory for your job, but does not by itself prevent another job from simultaneously using whatever core/memory allocation remains free on the same physical machine, or in some scheduler configurations, sharing the same memory subsystem even if core allocation is kept separate.

**Conclusion:** the most consistent explanation, supported by the evidence above, is memory-bandwidth contention from co-located jobs belonging to other users, not a hardware or configuration difference specific to CN-099. This is a property of running on a shared, multi-tenant cluster, not a flaw in this case's setup.

### 3.3 Practical implication

Because of this finding, single-run wall-clock numbers on Vanda cannot be trusted at face value without corroboration. Every decomposition and binding comparison in this study was structured to either (a) run all compared configurations back-to-back within one PBS job on one node, so that even if that node happened to be contended, all configurations in that comparison were penalized equally and their *relative* ranking is still meaningful, or (b) be explicitly cross-checked with repeats on multiple different nodes before drawing a conclusion.

For the actual scored 4-node run (the one whose result counts for the competition), this means: budget for at least one full repeat of the final configuration rather than trusting a single measurement, and if the target contest supercomputer (Gadi or ASPIRE-2A) supports requesting exclusive node access (commonly `place=excl` in PBS, or an equivalent flag), requesting it would remove this specific confound entirely for the scored run.

---

## 4. MPI rank-binding sweep

### 4.1 Method

As explained in §0.5, `I_MPI_PIN_DOMAIN core` fixes each MPI rank to exactly one physical core, and `I_MPI_PIN_ORDER` controls *which* core each rank number gets assigned to. Five named strategies (plus a same-setting repeat, for a noise check) were tested on the winning decomposition shape from §2 (`hierarchical (18 4 1)`), with all six experiments run back-to-back within a single PBS job on one node (**CN-130**), deliberately eliminating the node-to-node contention confound identified in §3, since every strategy in this comparison experienced identical conditions.

| Binding strategy | s / step | Δ vs. fastest |
|---|---:|---:|
| `bunch` | 9.0889 |, |
| `compact` | 9.0923 | +0.04% |
| `compact` (repeat) | 9.0951 | +0.07% |
| `nopin` (`I_MPI_PIN disable`) | 9.1179 | +0.32% |
| `scatter` | 9.1515 | +0.69% |
| `spread` | 9.1890 | +1.10% |

### 4.2 Confirming the mechanism directly, not just from timing

Rather than guessing why the timings differ, the actual rank-to-core assignments were extracted directly from each run's Intel MPI startup log (enabled via the `I_MPI_DEBUG=4` diagnostic setting, which prints a `===== CPU pinning =====` table listing every rank and the exact CPU core number it was bound to).

**Result:** on this specific 72-core, 2-socket topology, `compact`, `bunch`, and `spread` all produced the **exact same** rank-to-core mapping, rank 0 → core 0, rank 1 → core 2, rank 2 → core 4, ... continuing to fill every core on socket 1 (ranks 0–35), then rank 36 → core 1, rank 37 → core 3, ... filling socket 2 (ranks 36–71). This was confirmed with a direct line-by-line `diff` of the pinning tables: only the process ID numbers differed between runs (an unavoidable artifact of each run starting new processes); every single core assignment matched exactly.

`scatter` produced a genuinely different mapping, with no simple pattern, for example, rank 0 → core 0, rank 1 → core 25, rank 2 → core 48, rank 3 → core 49, deliberately avoiding placing consecutive rank numbers near each other.

`nopin` showed every rank's CPU affinity (the set of cores the operating system is *allowed* to run that process on) listed as the full set of all 72 cores, rather than a single core, direct, in-log confirmation that no fixed pinning was applied at all under this setting. The OS scheduler remains free to run, and potentially move, each rank across any of the 72 cores for the entire duration of the job.

### 4.3 Interpretation

Because `compact`, `bunch`, and `spread` were shown to share an **identical** physical core mapping, the small timing differences between them (9.089 to 9.189 s/step, about 1.1% spread) cannot be explained by placement at all, since the placement was literally the same. This is therefore the cleanest possible direct evidence of this configuration's true noise floor on a single, uncontended node: even with zero difference in where any rank physically ran, repeated measurements spread by about 1.1%. `scatter`'s result (9.152), despite its genuinely different rank placement, falls within that same 1.1% noise band and cannot be confidently distinguished from it.

**Conclusion:** for this workload, at 72 ranks on 72 cores, MPI pin *order* has no measurable effect on performance on this hardware, three of the four distinctly-named Intel MPI strategies turned out to be the same physical layout in disguise (confirmed directly from the logs, not inferred), and the one strategy that is genuinely different (`scatter`) performed statistically the same as the rest. `nopin` also performed within the same noise band over this 40-iteration test, but because its affinity mask allows migration for the entire run, and this test only ran 40 iterations (the scored 4-node run will run 150), it is not possible to rule out that unpinned ranks could drift to worse placements, or suffer cache-locality loss from migration, over a longer run. This risk was not tested and is flagged as open rather than dismissed.

### 4.4 Selected configuration

```
I_MPI_PIN_DOMAIN=core
I_MPI_PIN_ORDER=compact
```

`compact` is chosen over `bunch`/`spread` (statistically indistinguishable, and `compact` is the more conventional, widely-recognized name for this behavior) and over `nopin` (no measured advantage, and an unverified migration risk at longer run duration) primarily for reproducibility and conventionality, not because it demonstrated a measurable performance win over its closest alternatives, which it did not.

---

## 5. A note on OpenFOAM's built-in profiler

**What was attempted:** OpenFOAM v2512 includes a built-in `profiling` feature (enabled via a `profiling { active true; ... }` block in `controlDict`) intended to record an internal breakdown of where solver time is spent, e.g. how much time goes to the pressure-solve step versus the momentum-solve step versus MPI communication waits, as opposed to only the single external "average time per step" number used throughout this study.

**What went wrong:** by reading the relevant OpenFOAM v2512 source code directly (`Time.C`'s `setMonitoring()` function and `profiling.C`'s `stop()` function), it was confirmed that the `profiling` object is registered with the `AUTO_WRITE` flag, OpenFOAM shorthand meaning "only save this data to disk during a normal output-writing event." Every timing run in this study deliberately used `controlDict.noWrite` (see §1) specifically to exclude file I/O from the measured time, and one consequence of that file's `writeInterval 100000` setting is that, across a 40-iteration run, no output-writing event ever occurs. As a result, the profiler's data was collected internally in memory the whole time, but silently discarded (never written to any file) when each run ended, confirmed directly: `profiling::stop()` in the source code simply discards the in-memory data object; it does not force a write regardless of `writeInterval`.

**What would be needed to actually use it:** OpenFOAM v2512 provides an alternate settings file, `controlDict.withWrite`, that does enable periodic output writes. Building a profiling run from that file instead would let the profiler's data reach disk, but doing so introduces real file I/O time into the measured wall-clock result, making any such run **incomparable** to every number reported in this document, all of which were deliberately I/O-free. This was identified as a valuable follow-up but was not pursued within this study, specifically to avoid contaminating the timing comparisons already gathered.

---

## 6. Summary and recommended configuration

| Parameter | Value | Confidence |
|---|---|---|
| Decomposition method | `hierarchical` | High, chosen for determinism/reproducibility (§0.3), not only speed |
| `nHierarchical` (decomposition shape) | `(18 4 1)` | Medium-high, confirmed fastest on two independent clean nodes (§2.2) |
| `I_MPI_PIN_DOMAIN` | `core` | High |
| `I_MPI_PIN_ORDER` | `compact` | High, statistically tied with `bunch`/`nopin`, chosen for reproducibility and to avoid `nopin`'s unverified migration risk |

**Headline finding:** node-to-node contention on Vanda's shared scheduler (§3) produced a wall-clock swing of roughly 90% between the slowest and fastest nodes measured, far larger than the effect of decomposition shape (at most ~6.5% between shapes tested) or MPI binding strategy (at most ~1.1%, indistinguishable from measurement noise). For anyone presenting or extending this work: tuning decomposition and binding is worthwhile and produces real, if modest, gains, but on a shared multi-tenant cluster, accounting for (and budgeting repeats around) contention matters considerably more.

---

## 7. Recommendations for the scored 4-node run

1. Carry forward `hierarchical` decomposition with an `nHierarchical` triplet derived from the `(18 4 1)` per-node ratio established here, but re-validate it at actual 4-node scale rather than assuming it extrapolates linearly with node count.
2. Use `I_MPI_PIN_DOMAIN=core`, `I_MPI_PIN_ORDER=compact` for MPI rank placement.
3. Budget for at least one full repeat of the final 4-node configuration before treating any single run's number as the official reported result, given the contention risk directly demonstrated in §3.
4. If the target contest supercomputer (Gadi or ASPIRE-2A) supports requesting exclusive-node scheduling, request it, this would remove the shared-tenancy confound entirely for the scored run, which Vanda's default scheduling policy does not provide.
5. If deeper internal (solver-stage / MPI-wait) profiling is wanted for a presentation's technical-depth discussion, run it as a clearly separate, `controlDict.withWrite`-based diagnostic pass, kept apart from the I/O-free performance-comparison numbers reported in this document (§5).

---

## Appendix: glossary quick-reference

| Term | Meaning |
|---|---|
| Cell | A small 3D volume element making up the simulation mesh; this case has 65 million |
| Rank | One copy of the solver program, assigned to one portion of the split-up mesh, running on one CPU core |
| MPI | The standard protocol used to run many ranks in parallel and let them exchange data |
| decomposePar | The OpenFOAM utility that splits the mesh into per-rank pieces before a parallel run |
| Decomposition shape `(Nx Ny Nz)` | The number of mesh cuts along the x, y, and z axes under the `hierarchical` method |
| Processor face | A mesh face on the boundary between two ranks' sub-domains, requiring data exchange every iteration |
| Node | One physical server in the cluster, containing multiple CPU cores |
| Socket | One physical CPU chip; this study's nodes have two sockets, 36 cores each |
| NUMA | The property that memory attached to one socket is slower to access from the other socket |
| Pinning / binding | Explicitly fixing which physical core each MPI rank runs on for the whole job |
| `I_MPI_PIN_DOMAIN` / `I_MPI_PIN_ORDER` | Intel MPI's environment variables controlling pinning unit and rank-to-core order |
| s/step | Seconds of wall-clock time per solver iteration, the primary metric used throughout |
| Noise floor | How much an unchanged configuration's timing varies purely from run-to-run system randomness |
| PBS / `qsub` / `qstat` / `pbsnodes` | The job scheduler used on Vanda, and its job-submission, status-check, and node-inspection commands |
| `place=free` vs `place=excl` | PBS scheduling policy controlling whether other users' jobs may share your allocated node |
