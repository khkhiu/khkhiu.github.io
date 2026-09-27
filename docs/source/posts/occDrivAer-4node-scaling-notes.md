---
title: "OpenFOAM HPC Challenge: A 16% Performance Regression Caused by Scheduler Node Placement"
date: 2026-09-27
tags: [hpc, openfoam, pbs, cfd, performance]
---

# OpenFOAM HPC Challenge (OHC-1): Diagnosing a Silent 16% Performance Regression from Scheduler Node Placement

*Published: 2026-09-27*


*Working notes from preparing the OpenFOAM HPC task for the APAC HPC-AI 2026 Competition. This post covers the competition itself, the OHC-1 benchmark the task is derived from, the physical structure of the occDrivAer case, and the decomposition / renumbering / compiler / MPI settings we identified as worth testing.*

## Summary

While benchmarking the **occDrivAerStaticMesh** case (OHC-1, 65M-cell coarse mesh, `simpleFoam`) on NUS's Vanda PBS Pro cluster, a scored 4-node/288-rank run silently landed on **GPU-pool compute nodes** instead of the intended dedicated CPU nodes. This produced a run that *looked* successful — correct iteration count, correct force-coefficient convergence — but ran **16% slower** than an otherwise-identical run on dedicated CPU hardware. No error was raised anywhere in the pipeline; the only symptom was a worse number.

This post documents the case setup, the two independent CPU-node baseline runs, the misdirected GPU-node run, and the root-cause investigation that identified two concrete, evidence-backed contributors to the regression: **node co-tenancy (shared cores)** and a **separate network fabric** for the GPU node pool.

---

## Background

- **Task**: OpenFOAM HPC Challenge, occDrivAerStaticMesh (65M-cell coarse mesh), `simpleFoam` solver
- **Target metric**: `Average wall-clock time per time step`, lower is better, measured on the 4-node scored configuration
- **Scaling rule**: 40 iterations at 1 node, 80 at 2 nodes, 150 at 4 nodes
- **Software**: OpenFOAM v2512 (openfoam.com), built with Intel compilers 2024.2.0 + Intel MPI 2021.13.0
- **Cluster**: NUS Vanda, PBS Pro scheduler, 2× Intel Xeon 8452Y (Sapphire Rapids) per CPU node, 72 cores/node, 512 GB RAM
- **Decomposition**: `hierarchical`, 288 ranks, `nHierarchical (48 6 1)`

---

## Baseline: Two Independent, Correctly-Pinned CPU Runs

Two 4-node runs were executed on genuine CPU compute nodes (`node_pool=cpu_node`), using the identical `Allrun` script, decomposition, and `caseDefinition`.

| Job ID | Nodes used | Cd @ iter 150 | Avg. wall-clock/timestep |
|---|---|---|---|
| **1399773** | CN-057, CN-160, CN-041, CN-045 | 0.27917 | **2.4884 s** |
| **1402680** | CN-092, CN-104, CN-130, CN-142 | 0.27917 | **2.5095 s** |

Both runs:
- Reached `Time = 150` (full scoring run length)
- Reported `nProcs : 288`
- Produced bit-identical `Cd` at iteration 150 (0.27917), consistent with the published OHC-1 hardware reference range for 150 steps (~0.28–0.29: Huawei 0.289, Wikki 0.287, UniBwM 0.284, BAW 0.292)
- Showed excellent decomposition balance: max rank cell count 226,865 vs. average 226,856.8 (**0.0036% imbalance** across 288 ranks)

The spread between the two CPU runs is **0.85%** — normal run-to-run variance from node placement and momentary network conditions, and a good indicator of measurement noise for this configuration.

Preparation-chain timings (job 1399773):

| Stage | ExecutionTime | ClockTime |
|---|---|---|
| decomposePar | not logged by this OpenFOAM build for this stage | — |
| renumberMesh | 4.69 s | 7 s |
| potentialFoam | 10.95 s | 11 s |
| applyBoundaryLayer | 2.95 s | 4 s |
| simpleFoam (150 iters) | — | 2.4884 s/timestep avg |

---

## The Anomaly: A Run That "Passed" but Was 16% Slower

A later 4-node/288-rank run (**job 1402562**) completed with `Exit_status = 0`, reached the correct iteration count, and produced the identical `Cd = 0.27917` — every correctness check passed. But its performance was markedly worse:

> **Average wall-clock time per time step = 2.8812 s**

Compared to the 2.4884–2.5095 s baseline, this is a **~16% regression**, with no error message anywhere in the logs to explain it.

### Finding the cause: wrong node pool

```
$ qstat -xf 1402562.stdct-mgmt-02 | grep exec_host
exec_host = GN-A40-048/0*0+GN-A40-058/0*0+GN-A40-059/0*0+GN-A40-061/0*0
```

The job had been scheduled onto **`GN-A40-*` nodes** — NVIDIA A40 GPU-pool nodes — not the `CN-*` dedicated CPU nodes used by the two baseline runs. The job's PBS submission had specified `select=4:ncpus=72:mpiprocs=72:ompthreads=1:mem=500gb` with no explicit `queue` or node-pool constraint, and the site's routing queue silently placed a CPU-only OpenFOAM job onto the GPU pool — a pool the job never asked to use, and where it used none of the available GPUs.

Nothing in the OpenFOAM logs, the PBS exit status, or the force-coefficient convergence indicated anything was wrong. Only the raw timing number was worse — the kind of regression that is very easy to submit by accident in a benchmarking campaign.

---

## Root-Cause Investigation

Two hypotheses were tested against `pbsnodes -a` output for the exact nodes involved.

### 1. Node co-tenancy — confirmed

```
$ pbsnodes -a  (block for gn-a40-048)
resources_assigned.ncpus = 48
resources_assigned.mem   = 349175808kb
jobs = 1402621.stdct-mgmt-02/0 ... /35  (listed across two task-slot ranges)
```

At the time the benchmark ran, **48 of `gn-a40-048`'s 72 cores were already allocated to a different job** (1402621) — i.e., the node was shared between two concurrent workloads. By contrast, the equivalent check on the CPU baseline nodes at the time of their runs showed:

```
resources_assigned.ncpus = 0
```

— fully dedicated to the benchmark job, with no co-tenant. GPU-pool nodes on this cluster run in `sharing = default_shared` mode more aggressively than the dedicated CPU pool, exposing a CPU-only job to last-level-cache and memory-bandwidth contention from an unrelated co-resident job. This is a well-established, large-magnitude source of slowdown for memory-bandwidth-sensitive CFD codes and is the strongest, most directly evidenced explanation for the regression.

### 2. Separate network fabric — plausible contributing factor

```
GPU node (gn-a40-048):        switch = gcid-03, gpu_all
CPU nodes (cn-092/104/130/142): switch = ccid-07/08/09/10, cpu_all
```

GPU and CPU nodes sit on **entirely separate network fabrics** (`gpu_all` vs. `cpu_all`), not merely different switches within one fabric. `simpleFoam`'s SIMPLE loop performs an MPI collective (`Allreduce`/`Gather` inside the GAMG pressure solve) on every single iteration across all 288 ranks. Any difference in collective latency or bisection bandwidth between the two fabrics compounds directly into per-timestep wall-clock time over 150 iterations. This was not independently micro-benchmarked (e.g. with OSU latency/bandwidth tests on each fabric), so its exact contribution is not quantified — it is presented here as a plausible secondary factor, not a proven one.

### Conclusion

The 16% regression is best explained primarily by **CPU/memory-bandwidth contention from an unrelated co-tenant job sharing the same physical node**, with a **topologically distinct GPU-pool network fabric** as a plausible secondary contributor. Neither factor was visible from the solver's own output — both required inspecting the PBS scheduler's live node-resource state (`pbsnodes -a`) alongside the job's own `exec_host`.

---

## The Fix

Add an explicit resource constraint to the PBS job submission to force placement onto the dedicated CPU pool:

```bash
#PBS -l select=4:ncpus=72:mpiprocs=72:ompthreads=1:mem=500gb:node_pool=cpu_node
```

`node_pool=cpu_node` was confirmed as the correct attribute value by cross-referencing `pbsnodes -a` for a node from a known-good baseline run:

```
$ pbsnodes -a  (block for cn-160, used in job 1399773)
resources_available.node_pool = cpu_node
```

versus the GPU node:

```
$ pbsnodes -a  (block for gn-a40-048, used in job 1402562)
resources_available.node_pool = gpu_node
```

A minimal dry-run test (`/bin/hostname` job with the same resource request) confirmed the fix before committing a full-length run:

```bash
qsub -l select=4:ncpus=72:mpiprocs=72:ompthreads=1:mem=500gb:node_pool=cpu_node \
     -l walltime=00:02:00 -P <project> -- /bin/hostname
```
```
exec_host = CN-092/0*0+CN-104/0*0+CN-130/0*0+CN-142/0*0   (dedicated CPU nodes)
```

The full benchmark was then resubmitted with the fix and reproduced a result consistent with the original CPU baseline (job 1402680, 2.5095 s/timestep — see table above), confirming the fix and closing out the investigation.

Note: an explicit `-q cpu_parallel` queue override was attempted first and rejected (`qsub: Access to queue is denied`); the working queue for this project remains the default-routed `batch_cpu`, and `node_pool=cpu_node` alone was sufficient to steer routing correctly — no explicit `-q` flag was needed or usable.

---

## Results Table (Final)

| Job ID | Node type | Nodes | Cd @ iter 150 | Avg. wall-clock/timestep | Notes |
|---|---|---|---|---|---|
| 1399773 | CPU (dedicated) | CN-057/160/041/045 | 0.27917 | **2.4884 s** | Baseline #1 |
| 1402680 | CPU (dedicated, pinned) | CN-092/104/130/142 | 0.27917 | **2.5095 s** | Baseline #2, `node_pool=cpu_node` fix verified |
| 1402562 | GPU pool (misplaced) | GN-A40-048/058/059/061 | 0.27917 | 2.8812 s | +16% regression, root-caused and excluded |

**Reportable 4-node scored result: ~2.49-2.51 s/timestep**, Cd converged to 0.27917 (within the expected ~0.28-0.29 reference band).

---

## A Secondary, Fully Resolved Issue: I_MPI_STATS and the Missing APS Binary

During the same investigation, an attempt to collect MPI-level communication statistics surfaced two unrelated, now-resolved failures worth recording for completeness:

1. **`I_MPI_STATS=10`** triggered Intel MPI's Application Performance Snapshot (APS) collector as a backend, which is not installed on this cluster:
   ```
   [proxy:0:0@CN-057] HYD_spawn: execvp error on file aps (No such file or directory)
   ```
   This is a hard dependency of the highest verbosity level, not a bug in the job script.

2. **`I_MPI_STATS=4`** (a lower verbosity level intended to avoid the APS dependency) instead produced a Hydra process-manager communication failure at 288-rank/4-node scale:
   ```
   [mpiexec@CN-003] cmd_bcast_root: error sending cmd 9 to proxy
   ```
   A clean control run with `I_MPI_STATS` removed entirely completed without error on the same script, which isolates `I_MPI_STATS` itself (even at level 4) as destabilizing to Hydra's proxy control channel at this scale on this Intel MPI build.

**Resolution:** MPI-level statistics collection via `I_MPI_STATS` was abandoned for this cluster/toolchain combination. OpenFOAM's built-in `profiling` function object was attempted as an alternative, but was found to be unsupported in this v2512 build (`Unknown function type profiling`) and produced no output — a build/version limitation rather than a configuration error. Communication-vs-compute profiling was therefore not obtained for this campaign; any future attempt should first confirm which function-object types are compiled into the specific v2512 build in use, and avoid `I_MPI_STATS` entirely on this cluster.

---

## Lessons Learned

1. **A "successful" job (`Exit_status = 0`, correct physics, correct iteration count) is not the same as a *valid benchmark run*.** Scheduler-level node placement can silently substitute hardware of a materially different class without producing any application-level error.
2. **Always verify `exec_host` against the expected node-pool/hardware class**, not just job completion status, before trusting a performance number — especially on clusters with mixed CPU/GPU node pools under shared routing queues.
3. **`pbsnodes -a` is the ground truth for node-pool identity and live contention.** Cross-referencing `resources_available.node_pool` and `resources_assigned.ncpus`/`jobs =` between a known-good and a suspect node is a fast, decisive way to root-cause an unexplained performance delta.
4. **Pin scheduler resource requests explicitly** (`node_pool=cpu_node` here) rather than relying on default routing-queue behavior, particularly for benchmark or competition submissions where hardware consistency matters as much as the number itself.
5. Two independent, correctly-pinned baseline runs (rather than one) gave enough of a variance estimate (0.85% spread) to confidently identify a 16% deviation as a genuine anomaly rather than ordinary noise — worth budgeting allocation for at least one repeat run on any scored configuration.
6. Not every profiling avenue pans out on a given cluster/toolchain combination — `I_MPI_STATS` and OpenFOAM's `profiling` function object both failed here for independent, cluster-specific reasons, and it was more productive to document and move past these than to keep spending allocation chasing them.
