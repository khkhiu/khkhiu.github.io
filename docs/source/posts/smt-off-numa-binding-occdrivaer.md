# Disabling SMT cut our OpenFOAM HPC Challenge runtime by 17%, on half the cores

**TL;DR:** While benchmarking the [Open-closed cooling DrivAer variant with Static Mesh](https://develop.openfoam.com/committees/hpc/-/tree/develop/incompressible/simpleFoam/occDrivAerStaticMesh) using OpenFOAM v2512 on a Zen3 EPYC node, switching from 128 MPI ranks (one per hardware thread, SMT enabled) to 64 ranks (one per physical core, SMT disabled, explicit NUMA-aware binding) cut wall-clock time from **~43h12min to 36h04min**  **A ~17% reduction using half the rank count**, chaning only scheduling and memory placement did.

```{note}
This is a working-notes-style writeup from a live benchmarking session, not a
polished paper. Numbers are single-run observations on shared, non-exclusive
cluster nodes.  Hence please do not view this as a controlled A/B result with error bars.
```

## Background

`occDrivAerStaticMesh`'s geometry is a full car body derived from the notchback Ford Open Cooling DrivAer (OCDA). Adding a more complex underbody and engine-bay cooling channels than the original DrivAer model it is based on. For this variant, the wheels are static (no rotation) and the cooling inlets are sealed shut, hence "open-closed cooling DrivAer" (occDrivAer). Full case source: [`occDrivAerStaticMesh` on the OpenFOAM HPC committee repo](https://develop.openfoam.com/committees/hpc/-/tree/develop/incompressible/simpleFoam/occDrivAerStaticMesh).

The actual targets are **Aspire2A** and **Gadi**, both PBS Pro clusters we do not yet have access to yet. In the meantime, we have been using NUS SoC's Slurm-based compute cluster as a stand-in, picking the closest available hardware match:

| Target | CPU | Microarch | Cores/node | RAM/node | Closest SoC match |
|---|---|---|---|---|---|
| **Aspire2A** | 2× AMD EPYC 7713 | Zen3 "Milan" | 128 | 512GB DDR4 | `xcnf` (1× EPYC 7763, same Zen3 gen, 128 threads, 1TB) |
| **Gadi** | 2× Intel Cascade Lake (24-core) | Cascade Lake | 48 | 192GB | `xcne` (2× Xeon Gold 6230, 40 physical cores, 768GB) |

This post covers the `xcnf`/Aspire2A track.

## The experiment

Our first working baseline used the competition's default rank-per-thread convention: `xcnf` has 64 physical cores and exposes 128 logical CPUs via SMT2 (AMD's hyperthreading), and the original `Allrun` script requested `--ntasks=128 --ntasks-per-node=128` — one MPI rank per hardware thread, with no explicit process binding.

After that baseline completed (in a timeout-recovery run, see [Known issues](#known-issues-and-open-items) below), we tested a variant with SMT disabled and explicit core/NUMA binding:

```diff
- #SBATCH --job-name "occDrivAer_xcnf_aspire2a-baseline"
- #SBATCH --ntasks=128
- #SBATCH --ntasks-per-node=128
+ #SBATCH --job-name "occDrivAer_xcnf_aspire2a_smt64"
+ #SBATCH --ntasks=64
+ #SBATCH --ntasks-per-node=64
...
- OMPI_FLAGS=""
+ OMPI_FLAGS="--bind-to core --map-by numa"
```

Everything else — mesh, `fvSolution.fixedIter`, `controlDict.noWrite`, the OpenMPI vader/CMA fix (`OMPI_MCA_btl_vader_single_copy_mechanism=none`, more on that below), and the 4000-iteration `endTime` — was held identical between the two runs.

## Result

| Config | Ranks | Wall-clock | Nodes | Status |
|---|---|---|---|---|
| SMT on (baseline) | 128 (1/thread) | **43h12m** | `xcnf11` | COMPLETED (after a timeout/resubmit — see below) |
| SMT off + core/NUMA binding | 64 (1/core) | **36h04m** | `xcnf11` | COMPLETED, 4000/4000 iterations |

That is a **~17% wall-clock reduction while using half as many MPI ranks.**

## Why it is faster

`xcnf` is a single-socket AMD EPYC 7763: 64 physical cores, 128 threads via SMT. SMT threads sharing a physical core that do not get separate execution resources. They share the core's floating-point/integer units, L1/L2 cache, and path to memory. That is a beneficial for workloads with a lot of stalls (a second thread fills idle cycles while the first waits on memory), nut a net loss for workloads that are already saturating the core's cache/memory bandwidth (the second thread just adds contention).

`simpleFoam`'s dominant per-iteration cost is the **GAMG multigrid solve for pressure**, a sparse, irregular-access-pattern computation that's characteristically memory-bandwidth and cache-bound rather than compute-bound. Running two independent MPI ranks per physical core means two GAMG solves competing for the same L2 slice and memory path, on top of doubling the number of halo-exchange messages per iteration (same total data volume, smaller and more numerous packets, more MPI overhead) without doubling any useful throughput. Removing SMT gives each rank the whole core to itself; `--bind-to core` stops ranks migrating mid-run (which would otherwise reset per-core cache state); `--map-by numa` keeps each rank's memory local to its socket.

```{important}
`xcnf` is single-socket, so `--map-by numa` had limited room to matter here.
Aspire2A's actual nodes are **dual-socket** EPYC 7713. Hence, we expect the
core-binding win to transfer directly, but the NUMA-locality win to matter
*more* there, since cross-socket memory access is a real penalty that a
single-socket node simply does not have. This needs its own validation once
Aspire2A access is granted.
```

The size of the win (17%, not a much larger number) is consistent with only part of total wall-clock being spent in the GAMG-dominated inner loop. Mesh setup, halo exchange, and I/O phases are not SMT-sensitive in the same way, which caps how much overall speedup a purely compute/cache-contention fix can deliver.

## Validating that the physics remained consistent

A rank-count and decomposition change is exactly the kind of thing that *could* silently change results. Different load balance, different effective GAMG agglomeration levels, a partition boundary landing somewhere different in the wake. So before trusting the 17% number as "safe," we checked whether the two runs actually agreed on the aerodynamics.

The naive check, diffing the last 20 rows of the instantaneous drag-coefficient log, looked alarming at first: individual values differed by up to ~2%, and one moment-coefficient column even flipped sign between runs. Before concluding anything was wrong, we walked back through a few possible explanations:

1. **Was this actually two different runs, or a stale/duplicated file?** A `solverInfo.dat` residual log turned out to be byte-identical between the two case directories, same inode-different, but identical `md5sum`. Investigation showed this was a coincidence: the file's timestamp predated the run's completion by nearly 12 hours in both directories, meaning it was a stale leftover from case initialization in *both* runs, not something either job actually wrote during its solve. A separate, live-updating output (`coefficient_0.dat`, the actual per-iteration force-coefficient data) confirmed both jobs really did execute independently and completed fully.

2. **Was the case setup actually identical?** Diffed `forceCoeffsAll` (reference point, patches, direction vectors) between the two directories: zero differences.

3. **Was the Cd difference real, or an artifact of comparing single instantaneous iterations?** Plotting the per-iteration difference between the two runs' Cd traces showed a clear oscillation: an alternating sign, ~14–16 iteration period, amplitude ~±0.005–0.007. That is consistent with unsteady wake/shedding behavior that a steady-state SIMPLE solve never fully damps out, not with a genuine discrepancy. Averaging over a wider window (last 2000 iterations instead of the last 20) collapsed the gap between the two runs' mean Cd from 0.0016 down to **0.00062**. Smaller than the measured single-step noise floor (0.00069).

**Conclusion: the two configurations produce statistically indistinguishable aerodynamic results.** The speedup is a pure scheduling and memory-placement effect, not a change in what was being computed.

(Two other issues surfaced and were ruled out along the way: a suspected OpenMPI vader/CMA shared-memory bug that had caused a 21GB log flood and an OOM kill in an earlier run. This was confirmed fixed, zero recurrences in the SMT-off run's 5MB log, and a memory over-provisioning issue, `--mem=700G` requested against ~131GB actually used, now trimmed to a more realistic value for future submissions.)

## Known issues and open items

- **`solverInfo.dat` stalls at iteration 511** in every run so far (both the baseline and the SMT-off run). This is a pre-existing case-template quirk, not caused by this change. Does not affect `coefficient_0.dat` or job correctness, but residual-based convergence tracking via that file specifically is not currently usable. Root cause not yet located (likely a stale `writeInterval`/`timeStart` somewhere in the function-object include chain).

- **No checkpointing.** `controlDict.noWrite`'s `writeInterval` is larger than the total iteration count, so a timeout or crash means a full restart from iteration 0. Accepted as a tradeoff for now; worth reconsidering for longer multi-node runs where timeout risk is higher.

- **Single-socket validation only.** As noted above, the NUMA-binding half of this result is under-tested relative to what Aspire2A's dual-socket topology will actually need.

## Next up

We are now running the same SMT-off, core-bound, NUMA-mapped configuration at 2-node scale (128 total ranks, 64/node) to start building out the 1/2/4-node scaling curve the competition itself will require, before eventually porting the whole `Allrun` from Slurm's `#SBATCH` syntax to PBS Pro's `#PBS` directives for the real Aspire2A/Gadi submission.

---

*Setup: `occDrivAerStaticMesh`, OpenFOAM v2512 (built from source), coarse mesh (65M cells), NUS SoC compute cluster, `xcnf` partition (AMD EPYC 7763).*
