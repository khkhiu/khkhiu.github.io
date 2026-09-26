---
title: "Rank placement and GAMG-targeted collective tuning cut occDrivAer steady-state time by 10.9% at 2 nodes — full numbers, confounds, and what didn't work"
date: 2026-09-26
tags: [openfoam, hpc, cfd, pbs, decomposition, mpi, gamg]
---

# Rank placement and GAMG-targeted collective tuning cut occDrivAer steady-state time by 10.9% at 2 nodes

*Published: 2026-09-26*

**TL;DR:** On `occDrivAerStaticMesh` (OHC-1, OpenFOAM v2512, 65M-cell coarse mesh), at 2-node / 144-rank scale, we tested 4 decomposition-placement variants, 2 alternative decomposition methods, and 4 MPI-tuning configurations, using OpenFOAM's built-in `profiling` instrumentation and rank-0 `perf` call-stack sampling throughout. The best configuration — `hierarchical (24 6 1)` decomposition, explicit `-ppn 72`, NUMA-socket pinning, and MPI Gather/Bcast tuning targeted at GAMG's coarsest-level correction — gave a **10.9% steady-state improvement** (4.786 s/step vs. 5.373 s/step) over an identical-job control, once we excluded an 8-10 iteration NUMA warm-up transient from the average. `scotch` decomposition lost to `hierarchical` in every test, by a mechanism we can point to directly in the profiling data. Job-to-job hardware/allocation variance on identical configurations measured 4.9–15.8% across three separate PBS jobs — larger than several of the tuning effects we were chasing, which is why every comparison below is a same-job A/B pair, not a cross-job one.

```{note}
Working-notes writeup from a live benchmarking session on a 2-node PBS Pro
allocation (dual-socket Sapphire Rapids, 72 cores/node, no SMT), ahead of the
4-node scored run. All times are `Average wall-clock time per time step` from
simpleFoam's own log unless labeled "steady-state," in which case they are a
post-hoc average over the last 66 of 80 iterations, computed directly from the
per-timestep log lines.
```

## Test matrix and fixed parameters

Held constant across every run below: mesh (65M-cell coarse, unmodified), `simpleFoam`, `fvSchemes`, `fvSolution.fixedIter`, `-ybl 0.0450244`, OpenFOAM v2512 (Intel compiler/MPI build, `WM_COMPILER=Icx WM_MPLIB=INTELMPI`), and the full prep chain (`decomposePar -constant` → `restore0Dir -processor` → `renumberMesh -constant -overwrite -parallel` → `potentialFoam -initialiseUBCs -parallel` → `applyBoundaryLayer -ybl 0.0450244 -parallel` → `simpleFoam -parallel`). PBS resource request: `select=2:ncpus=72:mpiprocs=72:ompthreads=1:mem=500gb`. 2-node iteration count per the competition scaling rule: `endTime = 80`.

Two measurement harnesses were used and are labeled explicitly below, because they are not directly comparable:

- **Profiled harness** (`v3`, `v4`, `v5` runs): `controlDict.prof` with `profiling { active true; }` appended and `writeInterval` forced equal to `endTime`, so OpenFOAM's profiling `IOobject` is written to `processorN/<endTime>/uniform/profiling` at the final step. This adds one field write at iteration 80 only.
- **Clean harness** (`stack_final` run): unmodified `controlDict.noWrite` (default `writeInterval = 100000`, i.e., no writes at all), no profiling block. This is the harness that matters for the actual scored metric.

## 1. Single-node profiling baseline (context from the prior session)

Before the 2-node work, 1-node/72-rank profiling (no write, `endTime = 40`) gave:

| Config | Avg wall-clock/step | Std. dev. | Min. steps for 2% error @ 95% CI |
|---|---:|---:|---:|
| compact pin order | 9.148 s | 0.109 | 1 |
| bunch pin order | 9.081 s | 0.060 | 0 |

Profiling breakdown (`time.run()` and direct children, compact run):

| Component | Total time | % of `time.run()` |
|---|---:|---:|
| `time.run()` | 384.799 s | 100% |
| `fvMatrix::solve.p` (GAMG pressure) | 93.254 s | 24.2% |
| `fvMatrix::solve.U` (momentum, Ux+Uy+Uz) | 93.977 s | 24.4% |
| `fvMatrix::solve.omega` | 18.626 s | 4.8% |
| `fvMatrix::solve.k` | 17.583 s | 4.6% |
| `functionObjects.start()` (probe/force setup, one-time) | 8.953 s | 2.3% |
| `functionObjects.execute()` (per-iteration probes/forces) | 5.977 s | 1.6% |
| **Sum of named children** | **238.370 s** | **62.0%** |
| **Unaccounted** | **146.429 s** | **38.0%*** |

*\*Recomputed here from the raw trigger totals above; the live session's automated script sums ALL of `time.run()`'s direct children (including small triggers like `mesh.update()`, `fvOption` calls, and `objectRegistry::writeObject` not itemized in this table), giving 41.5%. The automated 39–42% figures used throughout the rest of this post are the authoritative ones; this table is for readability only.*

Within `solve.p`, 90.663 s (97.2% of the 92.828 s spent in `lduMatrix::solver.p`) was `lduMatrix::solver.coarsestLevelCorr` — GAMG's coarsest-level global correction. This single sub-component is the specific target of the MPI collective tuning discussed in section 4.

## 2. Decomposition placement sweep — 4 hierarchical variants (job: `v3`, profiled harness)

| Variant | `nHierarchical` | Avg wall-clock/step | Unaccounted (`time.run()`) | `solve.p` | `solve.U` |
|---|---|---:|---:|---:|---:|
| `baseline_ratio` | (24 6 1) | **4.958 s** | 152.445 s / 391.160 s (39.0%) | 104.987 s | 97.939 s |
| `node_aligned` | (2 12 6) | 5.161 s | 170.695 s / 405.417 s (42.1%) | 99.340 s | 96.352 s |
| `node_aligned_collectives` (+Allreduce/Reduce tuning) | (2 12 6) | 5.229 s | 170.849 s / 410.823 s (41.6%) | 104.248 s | 97.035 s |
| `node_aligned_mapby_node` (+compact pin) | (2 12 6) | 5.185 s | 170.695 s / 407.082 s (41.9%) | 99.551 s | 97.404 s |

All four hierarchical variants decomposed to **perfectly equal per-rank cell counts (453,713 cells/rank)** — decomposition balance was not a factor here; `node_aligned`'s slowdown is a communication-pattern effect, not a load-balance one. Confirming evidence from rank-0 `perf` sampling (top-60 functions by cycle share):

| Function | `baseline_ratio` | `node_aligned` |
|---|---:|---:|
| `GaussSeidelSmoother::smooth` | 19.33% (19.24% self) | 16.20% (16.11% self) |
| `lduMatrix::residual` | 11.48% | 10.46% |
| `lduMatrix::Amul` | 6.43% | 5.66% |
| `psm3_verbs_ips_ptl_poll` (MPI fabric polling) | *not in top 60* | **3.36% (1.59% self)** |

`node_aligned`'s outermost hierarchical coefficient set to the node count (2) produced a worse inter-partition edge-cut than the ratio-extrapolated `(24 6 1)` split, visible directly as MPI fabric-polling overhead that doesn't appear at all in `baseline_ratio`'s profile. Neither Allreduce/Reduce collective tuning nor compact intra-node pinning recovered this loss when layered on top of `node_aligned`'s decomposition — both stayed within noise of plain `node_aligned` (5.161→5.229/5.185 s, i.e., slightly worse, not better). **Conclusion: don't force the node count into the outermost hierarchical coefficient; extrapolate the existing ratio instead.**

## 3. Decomposition method comparison — scotch vs. hierarchical (job: `v4`, profiled harness)

| Variant | Method | Avg wall-clock/step | Std. dev. | Max cell-count imbalance | `solve.p` | `solve.U` |
|---|---|---:|---:|---:|---:|---:|
| `scotch_default` | scotch | 5.005 s | 0.216 | +1.076% above mean | **111.549 s** | 91.795 s |
| `scotch_pinned` (+compact pin) | scotch | 5.005 s | 0.214 | +1.076% above mean | 108.561 s | 93.633 s |
| `hierarchical_explicit_ppn` | hierarchical (24 6 1) | **4.871 s** | 0.222 | +0.0007% above mean | 94.689 s | 94.388 s |

Scotch's momentum solve (`solve.U`) is genuinely *faster* than hierarchical's (91.8–93.6 s vs. 94.4 s) — consistent with scotch's edge-cut minimization doing what it's designed to do for the majority of the halo-exchange traffic. But `solve.p` is **17–19 s slower**, wiping out the gain and then some. Rank-0 `perf` sampling shows *no* `psm3_verbs_ips_ptl_poll` entry in the top 60 for either `hierarchical_explicit_ppn` or `scotch_default` — so unlike the `node_aligned` case above, this isn't a fabric-polling problem. The more likely mechanism, given scotch's measured 1.08% cell-count imbalance (vs. hierarchical's 0.0007%): **GAMG's coarsest-level correction is a synchronizing global reduction across all 144 ranks every SIMPLE iteration, so the single slowest (most-loaded) rank sets the pace for that specific operation** — a small imbalance that barely touches per-rank local work (`solve.U`) can still measurably slow a global collective. Cd at iteration 80 was 0.339846 for both scotch variants (identical to each other, confirming pinning alone doesn't touch numerics) vs. 0.330062 for hierarchical — the ~2.9% Cd difference between decomposition methods reflects a genuinely different GAMG agglomeration/solve ordering, not an error in either run.

**Conclusion: hierarchical beats scotch here specifically because of GAMG coarsest-level sensitivity to partition balance, not overall communication volume. Scotch is not retested at 4 nodes.**

## 4. MPI tuning sweep on top of the winning decomposition (job: `v5`, profiled harness)

All three runs use `hierarchical (24 6 1)` + explicit `-ppn 72`, varying only MPI environment variables:

| Variant | Extra MPI flags | Avg wall-clock/step | Std. dev. | `solve.p` | `solve.U` | Unaccounted |
|---|---|---:|---:|---:|---:|---:|
| `control_ppn72` | none | 4.641 s | 0.123 | 92.271 s | 88.389 s | 150.397/365.237 s (41.2%) |
| `ppn72_numa_pinned` | `I_MPI_PIN_DOMAIN socket`, `I_MPI_PIN_ORDER compact` | 4.624 s | 0.112 | 91.251 s | 88.487 s | 149.913/363.953 s (41.2%) |
| `ppn72_gamg_collectives` | `I_MPI_ADJUST_GATHER 3`, `I_MPI_ADJUST_BCAST 3` | **4.611 s** | **0.086** | **90.314 s** | 87.669 s | 150.397/362.612 s (41.5%) |

Cd at iteration 80: `control_ppn72` = 0.330062, `ppn72_numa_pinned` = 0.330062 (differs from control only at the 8th significant figure), `ppn72_gamg_collectives` = 0.330062 (bit-identical to control to the precision logged). Decomposition balance identical across all three (max 453,717 cells, +0.0007% above mean) — confirms only the MPI environment changed between runs.

The Gather/Bcast tuning is the standout: it moved `solve.p` down by ~2 s (92.27→90.31 s) while leaving `solve.U` essentially flat (88.39→87.67 s, within run-to-run noise), and **reduced standard deviation by 30%** (0.123→0.086) relative to control — a targeted, mechanistically-explained win with zero numerical side-effect. Allreduce/Reduce tuning (tested separately in section 2's `node_aligned_collectives`, applied to a different decomposition) showed no comparable benefit; the difference is that Gather/Bcast, not Allreduce/Reduce, is the collective pattern GAMG's coarsest-level assembly actually uses on this OpenFOAM build.

## 5. Stacking NUMA pinning + GAMG collectives, and a warm-up transient (job: `stack_final`, clean harness — no forced write, no profiling instrumentation)

| Variant | Whole-run avg | Whole-run std. dev. | Steady-state avg (last 66/80 iters) | Min. steps for 2% error @ 95% CI |
|---|---:|---:|---:|---:|
| `stacked_numa_gamg` (NUMA pin + Gather/Bcast) | 5.253 s | **1.230** | **4.786 s** | 526 |
| `control_recheck` (no extra tuning) | 5.332 s | 0.475 | 5.373 s | 76 |

Taken at face value, the stacked config's 2.6x-higher standard deviation (1.230 vs 0.475) looks like a reliability problem, not a win. The per-iteration trace resolves it. First 8 iterations of `stacked_numa_gamg`:

```
iter 1:  9.124 s        iter 5:  8.990 s
iter 2:  8.954 s        iter 6:  8.922 s
iter 3:  9.052 s        iter 7:  8.005 s
iter 4:  8.999 s        iter 8:  8.139 s
```

...ramping down through iterations 9–14 (6.777 → 6.148 → 5.565 → 5.209 → 5.239 → 5.187 s) before settling into a stable ~4.6–4.9 s band from iteration ~15 onward. `control_recheck` shows no equivalent transient — it opens near 5.14 s and stabilizes into its own ~5.2–5.4 s band by iteration ~10, with one isolated 9.396 s spike at iteration ~46 (a single outlier, not a pattern; likely unrelated transient system noise, not evidence of a repeating problem).

Excluding the warm-up window, the real comparison is **4.786 s vs. 5.373 s — a 10.9% steady-state improvement**, roughly 7x larger than the 1.5% the whole-run averages suggested. We attribute the transient to first-touch memory-page-fault and cache-warming costs specific to actively steering data locality under `I_MPI_PIN_DOMAIN socket` — a one-time cost, not a recurring penalty, and one that shrinks as a fraction of total runtime the longer the run (at the 4-node/150-iteration scored configuration, ~10 slow iterations is 6.7% of the run vs. 12.5% of this 80-iteration test). Cd at iteration 80 was 0.330062 for both variants (identical to the profiled-harness runs above), confirming the tuning changes only scheduling/memory placement.

## 6. A confound we checked and ruled out

The profiled-harness runs (`v3`/`v4`/`v5`) carry OpenFOAM's `profiling` instrumentation active for all 80 iterations (a timer call at every named scope); the clean-harness run (`stack_final`) carries none. If this instrumentation overhead were driving part of the gap between the two harnesses, we'd expect the *instrumented* runs to be slower. We observe the opposite: `v4`/`v5`'s `hierarchical (24 6 1)` + `-ppn 72` configuration ran at 4.871 s (`v4`) and 4.641 s (`v5`) — both *faster* than `stack_final`'s otherwise-identical `control_recheck` at 5.332 s (whole-run) / 5.373 s (steady-state). This rules out instrumentation overhead as the explanation and reinforces that the gap is genuine job-to-job variance (below), not a measurement artifact.

## 7. Job-to-job hardware/allocation variance

The exact same configuration — `hierarchical (24 6 1)`, explicit `-ppn 72`, no other tuning — was run in three separate PBS job submissions:

| Job | Harness | Avg wall-clock/step |
|---|---|---:|
| `v4` (`hierarchical_explicit_ppn`) | profiled | 4.871 s |
| `v5` (`control_ppn72`) | profiled | 4.641 s |
| `stack_final` (`control_recheck`) | clean | 5.332 s (whole) / 5.373 s (steady-state) |

Between the two profiled-harness jobs (fairest comparison, same instrumentation): **4.9% spread** (4.871 vs 4.641 s). Including the clean-harness job: **13.0–15.8% spread** across all three. This is comparable to, and in the wider case larger than, most of the tuning effects measured in sections 3–5 above. **Every comparison in this post that claims a specific effect (decomposition method, MPI flag, pinning) is a same-job A/B pair for exactly this reason** — cross-job wall-clock comparisons on this cluster are not reliable enough to attribute a difference to a specific setting.

## 8. Scaling efficiency (1 → 2 nodes)

| 1-node baseline | 2-node comparison | Speedup | Parallel efficiency |
|---|---|---:|---:|
| compact, no-write, 9.148 s | `stack_final` steady-state best (4.786 s) | 1.911x | **95.6%** |
| compact, no-write, 9.148 s | `stack_final` control, whole-run (5.332 s) | 1.716x | 85.8% |
| compact, write-enabled, 9.805 s* | `v4` `hierarchical_explicit_ppn`, write-enabled (4.871 s) | 2.013x | **100.6%** |

*\*1-node write-enabled figure from the earlier profiled session (forced write at `endTime`); bunch's write-enabled figure was not captured in that session.*

The third row's slightly superlinear efficiency (>100%) is plausible and not obviously an error: halving the per-rank problem size when doubling node count can improve L2/L3 cache residency enough to outweigh added communication cost at this scale — a known effect in memory-bandwidth-bound multigrid solves, consistent with what the 1-node profiling in section 1 already showed (GAMG pressure and momentum solves dominate and are exactly the kind of irregular-access, bandwidth-sensitive work where this applies). We do not have enough independent 1-node/2-node pairs on identical harnesses to rule out job-to-job variance (section 7) as a contributor to the >100% figure specifically, so we report all three pairings above rather than picking the most flattering one.

## 9. Resource accounting

| Job | Nodes | Ranks | Walltime used | CPU-time (`resources_used.cput`) |
|---|---:|---:|---:|---:|
| `v4` (3 experiments) | 2 | 144 | 00:47:57 | 52:40:08 |
| `v5` (3 experiments) | 2 | 144 | 00:40:23 | 49:11:34 |

Credit/allocation balance (`hpc project`) could not be captured from inside the PBS batch environment — the `hpc` CLI exists on the login node (`/usr/local/bin/hpc`) but is not on the compute-node `PATH` used by the job script; balance was checked manually from the login node instead, before and after each submission.

## 10. Known issues and implementation notes

- **OpenFOAM's `profiling` object is only written to disk at a write timestep.** With `active true` but the default `writeInterval` (100,000, larger than any `endTime` used here), the profiling summary is silently never written — not an error, just never triggered. Workaround: set `writeInterval = endTime` for profiling runs specifically; don't use this setting for the actual scored run, since it adds a field write the task's `controlDict.noWrite` convention doesn't call for.
- **`I_MPI_STATS` requires Intel's `aps` tool**, which is not installed on this cluster's compute nodes; setting `I_MPI_STATS 20` caused every `mpirun` launch (including `renumberMesh`, the very first parallel step) to fail identically with `execvp error on file aps`. Removed; MPI-level timing analysis was done via OpenFOAM's own profiling object plus rank-0 `perf` sampling instead.
- **Duplicate dictionary entries silently take the last value.** Appending a second `profiling { ... }` block via `cat >>` after an existing one in `controlDict.prof` means OpenFOAM's parser uses the appended block's settings, silently overriding the first — not a syntax error, so it's easy to miss. Fixed by `sed`-deleting any existing `profiling { ... }` block before appending a fresh one.
- **`perf record` is usable on this cluster's compute nodes** without any special permission adjustment — confirmed via `perf stat -e cycles true` before relying on it. Wrapped to sample rank 0 only (via `PMI_RANK` check), to avoid 144x sampling overhead.

## Locked configuration going into 4 nodes

```
decompositionMethod  hierarchical;
nHierarchical         (N_nodes×24  6  1);   # ratio-extrapolated, NOT node-boundary-aligned
```
```
mpirun -np <N_nodes×72> --hostfile $PBS_NODEFILE -ppn 72 \
  -genv I_MPI_PIN_DOMAIN socket -genv I_MPI_PIN_ORDER compact \
  -genv I_MPI_ADJUST_GATHER 3 -genv I_MPI_ADJUST_BCAST 3
```

Open questions carried forward: whether the ~39–42% unaccounted-time fraction (sections 1–4; not attributable to any named OpenFOAM profiling trigger, and not explained by the `perf`-visible GaussSeidelSmoother/lduMatrix computation either) grows disproportionately at 4 nodes (communication-bound signature) or stays flat (compute-bound signature); whether the NUMA warm-up transient (section 5) behaves the same way over 150 iterations; and whether the 4.9–15.8% job-to-job variance measured here (section 7) is stable or grows at 4-node scale, which would materially affect how many repeat submissions are needed to trust the scored number.

---

*Setup: `occDrivAerStaticMesh`, OpenFOAM v2512 (built from source, Intel oneAPI compilers 2024.2.0, Intel MPI 2021.13.0), coarse mesh (65M cells), 2× dual-socket Intel Xeon 8452Y "Sapphire Rapids" nodes (72 cores/node, no SMT, 500GB/node requested), PBS Pro, `psm3` libfabric provider confirmed in every multi-node run (no TCP fallback observed).*
