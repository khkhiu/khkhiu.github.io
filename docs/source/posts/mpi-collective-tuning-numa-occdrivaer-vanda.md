---
title: "Rank placement and collective tuning cut our OpenFOAM HPC Challenge steady-state time by 11%, without touching decomposition physics"
date: 2026-09-26
tags: [openfoam, hpc, cfd, pbs, decomposition, mpi, gamg]
---

# Rank placement and collective tuning cut our OpenFOAM HPC Challenge steady-state time by 11%, without touching decomposition physics

*Published: 2026-09-26*

**TL;DR:** Benchmarking [`occDrivAerStaticMesh`](https://develop.openfoam.com/committees/hpc/-/tree/develop/incompressible/simpleFoam/occDrivAerStaticMesh) (OpenFOAM v2512) on a 2-node Sapphire Rapids allocation, we found that decomposition *method* barely mattered once load balance was controlled for — but explicit rank placement (`-ppn`), NUMA-socket pinning, and targeted MPI collective tuning for GAMG's coarsest-level correction combined for a genuine **~11% steady-state improvement**, once we controlled for a NUMA-pinning warm-up transient that a naive whole-run average would have hidden. Along the way we learned that node-to-node hardware variance on our test cluster (~13-15% between otherwise-identical jobs) is larger than most of the tuning effects we were chasing, which reshaped how we validate every result below.

```{note}
This is a working-notes-style writeup from a live benchmarking session, not a
polished paper. All comparisons below were re-run as same-job, same-allocation
A/B pairs specifically because we discovered cross-job comparisons on this
cluster are not reliable — see "A confound we didn't expect" below.
```

## Background

`occDrivAerStaticMesh` is the OpenFOAM HPC Challenge (OHC-1) case: a full closed-cooling DrivAer car body, static wheels, steady-state RANS via `simpleFoam`, benchmarked on the 65M-cell coarse mesh. The competition's scored run uses 4 CPU nodes on either Gadi or ASPIRE-2A (both PBS Pro), with iteration counts fixed by node count: 40 at 1 node, 80 at 2 nodes, 150 at 4 nodes.

We ran this benchmarking on a PBS Pro cluster with dual-socket Intel Xeon 8452Y (Sapphire Rapids, 36 cores/socket, 72 cores/node, no SMT) as a stand-in while waiting on the real competition clusters — close enough architecturally to be a useful proxy for the scaling and tuning questions below.

## What we tried, and what didn't matter

Before landing on the winning configuration, we ruled out several plausible optimizations:

- **Intra-node pin *order*** (`compact` vs `bunch`, tested at 1-node scale): no measurable difference. Unsurprising in hindsight — at 1 node everything communicates over shared memory regardless of order.
- **`scotch` decomposition** vs. `hierarchical`: scotch minimizes edge-cut directly, so we expected a win. It lost. Profiling explained why: scotch introduced a small load imbalance (~1.1% above average vs. hierarchical's ~0.0007%), and while scotch's momentum solve (`fvMatrix::solve.U`) was actually *faster* than hierarchical's, its pressure solve (`fvMatrix::solve.p`) — GAMG's coarsest-level correction, a global reduction — was ~17s slower per 80-iteration run. Net loss. **Lesson: GAMG's coarsest-level correction appears more sensitive to partition balance than momentum solve is**, so an edge-cut-optimizing method can lose overall even while winning locally.
- **MPI Allreduce/Reduce algorithm tuning** (`I_MPI_ADJUST_ALLREDUCE`/`REDUCE`): no effect.

## What did work

```diff
- mpirun -np 144 --hostfile $PBS_NODEFILE
+ mpirun -np 144 --hostfile $PBS_NODEFILE -ppn 72 \
+   -genv I_MPI_PIN_DOMAIN socket -genv I_MPI_PIN_ORDER compact \
+   -genv I_MPI_ADJUST_GATHER 3 -genv I_MPI_ADJUST_BCAST 3
```

Three changes, stacked:

1. **Explicit `-ppn 72`** — forcing exactly 72 ranks per node in contiguous blocks, rather than trusting the default hostfile-order mapping. This alone was a small, repeatable win once we moved from 1 to 2 nodes, where the ambiguity in default rank-to-node assignment actually starts to matter.
2. **NUMA socket pinning** (`I_MPI_PIN_DOMAIN socket`) — grouping neighboring ranks (in decomposition order) onto the same socket where possible, so cross-socket memory traffic is reduced for halo exchange.
3. **MPI collective tuning for Gather/Bcast** specifically (not Allreduce) — targeting the exact collective pattern GAMG's coarsest-level assembly uses. This showed up precisely where we'd predict: `fvMatrix::solve.p` time dropped consistently across repeated runs, while `fvMatrix::solve.U` stayed flat — a clean, mechanistically-explained result, not noise.

Gather/Bcast tuning alone was also, independently, a *variance reducer*: standard deviation of per-step wall-clock time dropped from 0.123s to 0.086s (a ~30% tighter spread) in one same-job A/B pair, with bit-identical drag-coefficient output — confirming the tuning changes only *how* the reduction communicates, not the numerics.

## A confound we didn't expect: node-to-node hardware variance

The same exact configuration, submitted as separate PBS jobs, gave us:

| Job | Config | Avg wall-clock/step |
|---|---|---:|
| Job A | hierarchical (24 6 1) + `-ppn 72` | 4.641s |
| Job B (same config) | hierarchical (24 6 1) + `-ppn 72` | 4.871s |
| Job C (same config) | hierarchical (24 6 1) + `-ppn 72` | 5.332s |

That's a **~13-15% spread from allocation alone** — larger than most of the individual tuning effects we were trying to measure. Once we saw this, we stopped trusting cross-job comparisons entirely and re-ran every remaining experiment as a same-job (same-allocation) A/B pair, with a fresh control run alongside every new variant in the same PBS submission. This is the only way we could confidently attribute an effect to a specific setting rather than to which physical nodes happened to get allocated.

## A result that looked worse until we looked closer

Stacking all three changes together (NUMA pinning + `-ppn 72` + GAMG collective tuning) against a same-job control gave us this at first glance:

| | Whole-run average | Standard deviation |
|---|---:|---:|
| Stacked config | 5.253s | **1.230s** |
| Control | 5.332s | 0.475s |

Faster on average, but 2.6x more variable — not obviously a config we'd want to lock in for a scored benchmark. Before writing this off, we pulled the raw per-iteration trace rather than trusting the summary statistic:

```{important}
The stacked run's first ~8-10 iterations ran at nearly 2x steady-state time
(~9.0s, ramping down through 8.0 → 6.8 → 6.1 → 5.6 → 5.2s), before settling
into a stable band around 4.65-4.9s/step for the remaining ~66 iterations.
The control run showed no such transient — it started near its steady-state
value and stayed there throughout.
```

Excluding the warm-up window, the real comparison is:

| | Steady-state average (last 66 iterations) |
|---|---:|
| Stacked config | **4.786s** |
| Control | 5.373s |

**~10.9% faster**, not the ~1.5% the naive whole-run average suggested — and the earlier "high variance" was entirely an artifact of averaging two different regimes together, not evidence the configuration is unreliable.

The mechanism is consistent with what we'd expect from NUMA-aware pinning specifically: first-touch memory page faults and cache warming take a few iterations to pay off when the runtime is actively steering data locality. It's a one-time cost, not a steady-state penalty — and at the competition's 150-iteration, 4-node scored configuration, that same ~8-10 iteration warm-up is a much smaller fraction of the total run than it was in our 80-iteration test here, which argues the win should be *more* valuable, not less, at the scale that actually counts.

## What we still don't have an explanation for

Across every configuration we tested, at both 1-node and 2-node scale, roughly **40% of iteration time falls outside any named OpenFOAM profiling trigger** — not `solve.p`, not `solve.U`, not the turbulence solves, not the function-object post-processing. `perf`-based call-stack sampling on rank 0 confirms real computation is happening (GaussSeidelSmoother and lduMatrix residual/Amul evaluation dominate the visible profile), but nothing in OpenFOAM's own instrumentation labels where that ~40% actually goes — most likely matrix assembly and boundary-condition evaluation between the named solves, plus any halo exchange that isn't wrapped in a profiling scope. This fraction held roughly steady between 1 and 2 nodes; whether it grows disproportionately at 4 nodes (which would point to communication) or stays flat (which would point to compute) is one of the open questions we're carrying into the next round.

## Validating that none of this changed the physics

Every configuration change above is a scheduling/communication-pattern change, not a numerical one, so we checked drag-coefficient output at each step rather than assuming. Where MPI tuning alone was varied (no decomposition change), Cd matched to 8+ significant figures between configurations — exactly what we'd expect, since none of these settings touch `fvSolution`, the mesh, or the solver itself. Where decomposition *method* changed (scotch vs. hierarchical), Cd differed at the 4th decimal place, consistent with the different GAMG agglomeration and solve ordering that a genuinely different partition produces — a normal, expected effect, not a red flag.

## Next up

We're carrying this configuration — `hierarchical` decomposition (ratio-extrapolated, not node-boundary-aligned), explicit `-ppn`, NUMA socket pinning, and Gather/Bcast collective tuning — into the 4-node, 150-iteration scored configuration next. Specific things we're watching for there: whether the unaccounted-time fraction grows with node count, whether the NUMA warm-up transient behaves the same way at 4 nodes, and whether `-ppn`'s benefit (which only became visible once we moved past 1 node) continues to compound as node count increases further.

---

*Setup: `occDrivAerStaticMesh`, OpenFOAM v2512 (built from source, Intel compilers/MPI), coarse mesh (65M cells), 2× dual-socket Sapphire Rapids nodes (72 cores/node, no SMT), PBS Pro.*
