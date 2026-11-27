---
title: "Fifteen turning points: what APAC HPC-AI 2026 taught us about tuning OpenFOAM"
date: 2026-11-27
tags: [openfoam, hpc, cfd, mpi, competition, aspire2a, gadi]
---

# Fifteen turning points: what APAC HPC-AI 2026 taught us about tuning OpenFOAM

*Published: 2026-11-27*

**TL;DR:** Team Kent Ridge finished the 9th APAC HPC-AI Competition with a Merit award. That result came out of a long chain of experiments on the OpenFOAM task, and the chain bent at fifteen points. Those turning points share one pattern: almost every belief we started with was overturned by measurement. The beliefs that fell were big ones. We thought hierarchical decomposition would win, that allReduce was the 4-node bottleneck, and that the MPI library was breaking our core binding. All three were wrong. The biggest gains came from diagnosis rather than tuning. Fixing rank pinning and fusing two passes over the solver's matrix each beat every MPI knob and compiler flag we tried, combined.

```{note}
These are working notes reconstructed from our session logs, not a controlled
study. They cover the OpenFOAM task only, which is the half I worked on. The
Qwen3-235B inference task was run by my teammates, and it appears here only
where it changed how the whole submission was framed. The fused-residual kernel
in turning point 12 was written by a teammate; my part was testing, porting and
profiling it.
```

## Background

The competition paired two workloads. One workload was Qwen3-235B inference on 16 GPUs. The other workload, the one these notes are about, was OpenFOAM's `simpleFoam` solving airflow over the `occDrivAerStaticMesh` car: 65 million cells, at 140 km/h, on four CPU nodes. Those four nodes could sit on either of two national supercomputers: NSCC Singapore's **ASPIRE 2A** or NCI Australia's **Gadi**. Both machines were open to us, so we ran full studies on both and picked one for the scored entry.

The scored entry is measured by one number: **average wall-clock time per time step**. That number has to come with a correct answer, which here means the drag coefficient (Cd) at the end of the run. Cd is checked in two ways, depending on which tier a change falls under:

- **Basic tier:** runtime settings, rank counts, decomposition, MPI transport and site builds. Basic runs only need to pass a loose sanity check against the reference case.
- **Bonus tier:** anything that changes code or floating-point behaviour. Bonus runs have to be compared against the team's own Basic run, and Cd has to stay within ±0.5% of it.

That tier boundary mattered more than we expected. It decided how two of our results were labelled, and it shaped what we presented.

The case itself was not new. It comes from the **first OpenFOAM HPC Challenge (OHC-1)**, a community benchmark that collected 237 valid submissions from 12 organisations. That history gave us a head start, and as turning point 1 shows, it also gave us a wrong assumption.

---

## Phase 0: Practice clusters (September to early October)

### 1. Hierarchical beat scotch on Vanda, and OHC-1 seemed to agree

Our first runs went onto Vanda, NUS's Sapphire Rapids practice cluster. Vanda let us compare the two decomposition methods we cared about: `hierarchical` and `scotch`. Those two methods split the mesh in very different ways. Hierarchical cuts the mesh geometrically, slicing it into boxes along x, y and z. Scotch treats the mesh as a graph and cuts it where the fewest connections cross between pieces. Each piece goes to one MPI rank, and every face that crosses between ranks is data that has to be exchanged on every iteration. On paper, then, scotch should communicate less.

Our early September numbers said the opposite:

| Method | 1 node | 2 nodes | 4 nodes |
|---|---|---|---|
| hierarchical | 10.25 s/step | 4.89 s/step | 2.84 s/step |
| scotch | 19.24 s/step | 5.31 s/step | 3.29 s/step |

The 1-node scotch figure looked suspicious. That suspicion came from the scaling it implied: 181% parallel efficiency from one node to two, which isn't physically plausible here. A plausible explanation is that the single 1-node scotch run was simply bad, through cold caches, contention, or an unlucky partition. Even with that run set aside, hierarchical still led at 2 and 4 nodes. A later controlled 2-node test kept it ahead (4.871 vs 5.005 s/step). That test also offered a reason: scotch left about 1% cell imbalance between ranks, while hierarchical's was essentially zero, and the solver's global steps wait for the most loaded rank.

That reason seemed to be backed by published data. The data came from the OHC-1 submission spreadsheets, which we read before spending any scored-cluster time. In those spreadsheets, every top hardware-track team that reported its method used hierarchical decomposition with RCM (reverse Cuthill–McKee) renumbering. RCM reorders cells so that neighbours sit close together in memory, which matters for a solver that spends most of its time waiting on memory. Nobody had won by switching to a graph partitioner.

**Why it was a turning point:** we concluded the method was settled and only the numbers needed tuning. That conclusion carried straight into our first plans for Gadi, which recommended a hierarchical `(52 8 1)` layout. Turning point 5 overturned it.

### 2. Shared nodes on Vanda taught us to measure noise first

Vanda's scheduler allowed other users' jobs onto the nodes we were using. Those shared nodes cost us about 16% on one run, which was larger than any optimisation we were testing at the time. That gap forced the question every later experiment had to answer first: how much does an unchanged configuration vary on its own?

On its own, an unchanged configuration varied a lot. Repeating the same job under the same harness moved the result by about 5%. Moving between our two measurement harnesses widened that to 13–16%. A spread that wide made most single-run comparisons meaningless, because a typical tuning change was worth a few percent at best.

A few percent also hid in the hardware we landed on. One job landed on a GPU node with a different CPU from the rest of the cluster. That node would have quietly produced a non-comparable number, so we added a CPU guard that aborted any job on the wrong processor within seconds.

**Why it was a turning point:** this is where our working rules came from. Those rules were: request dedicated nodes, record which nodes every job ran on, establish the noise floor before tuning, and only accept a change if it was faster by more than 1% across three repeats with Cd unchanged. Every later result in these notes was judged against those rules.

### 3. Profiling on the SOC cluster gave us a method, not just numbers

The method we used for the rest of the competition started on the School of Computing cluster. That cluster's 10 GbE network couldn't represent either scored machine's interconnect, so we used it only for single-node behaviour. Single-node behaviour turned out to be the most important thing to understand. We ran STREAM to find the memory-bandwidth ceiling, swept rank counts, and collected hardware counters with `perf`.

The counters told a consistent story. Above roughly 16 ranks, the solver was **memory-bound**: adding cores added little, because the cores were all waiting on the same memory bandwidth. That bandwidth limit explained a second finding: spreading ranks across the chip beat packing them together. Packed ranks crowd onto the same memory controllers, and spread ranks share the load.

That load picture became a plan we could carry anywhere: run, profile, optimise, repeat, at 1, 2 and then 4 nodes, changing one thing at a time. We wrote it so that every cluster-specific detail lived in a single environment file, and moved it unchanged to ASPIRE 2A and Gadi.

**Why it was a turning point:** from here on, the competition was a loop instead of a guess. The loop is also what made the next twelve turning points visible, because each one started as a profile that disagreed with what we expected.

---

## Phase 1: Scored clusters and the Basic tier (7 to 14 October)

### 4. ASPIRE 2A: ranks were losing their pinning

The loop's first run on ASPIRE 2A produced numbers that wouldn't sit still. Those numbers moved by 3–6% between identical runs, far more than ASPIRE's dedicated nodes should allow. That much movement pointed at something inside the job rather than outside it.

Inside the job, the ranks were wandering. ASPIRE's nodes have two 64-core AMD EPYC 7713 processors with simultaneous multithreading (SMT), so each physical core appears to Linux as two logical CPUs: CPU *n* and CPU *n*+128. We launched one rank per physical core and pinned each one, which means telling the kernel which CPU a rank may run on. That pinning wasn't holding. A sampling run found 96 of 387 sampled ranks sitting on CPUs numbered 128 or above, the SMT siblings of cores that already had a rank.

A rank sitting on a sibling shares one physical core with another rank. That sharing roughly halves both ranks' speed, and in this solver every iteration waits for the slowest rank. The slowest rank therefore set the pace for all of them. A small probe program printed each rank's CPU mask before and after `MPI_Init`. Before `MPI_Init`, the masks were correct; after it, every rank's mask had widened to all 256 logical CPUs.

All 256 CPUs open meant the scheduler was free to move ranks anywhere, so we took that freedom away again. Our team's script, `pin.sh`, re-applies each rank's binding with `taskset` every 0.2 seconds for the first 60 seconds of the run. Sixty seconds is long enough to outlast whenever the mask gets reset. The fix touches no source code, no libraries and no preloaded code:

| Nodes | Gain from re-pinning |
|---|---|
| 1 | 8.7% faster |
| 4 | 7.2% faster |
| Run-to-run noise | 4.7% → 0.3% |

That noise drop mattered as much as the speed. Speed was the headline, but noise was the enabler: at 0.3%, a 1% difference was finally real. Real differences need correct answers too, and Cd came out bit-identical with and without the fix.

**Why it was a turning point:** this was the biggest single gain of the competition, and it came from diagnosis rather than tuning. Before it, most of our ASPIRE comparisons had been lost in the noise. (Turning point 10 corrects our first explanation of *why* the masks were reset.)

### 5. Scotch overtook hierarchical on both scored clusters

The settled method from turning point 1 didn't survive the scored clusters. Those clusters reversed it on both machines. On ASPIRE 2A, scotch tied hierarchical at one node, then pulled ahead by about 3% at two nodes and 2–3% at four. Gadi showed the same pattern, with scotch's margin growing as node count rose.

That growth had a clear source in the decomposition logs. The logs showed scotch producing **40–50% fewer processor boundary faces** than the best hierarchical shapes. Fewer boundary faces mean less data crossing between ranks on every iteration, and that saving grows as more of the traffic has to cross the network between nodes. On Vanda's slower network the opposite effect, scotch's small cell imbalance, had dominated. On ASPIRE's and Gadi's faster interconnects, the communication saving won.

Winning communication was only half the configuration; rank count was the other half, and there the two machines disagreed:

- **ASPIRE 2A:** 448 ranks (112 per node, 14 per memory domain) beat a fully loaded 512 by 1.5% across three repeats. Leaving a core idle in each memory domain gave the remaining ranks more bandwidth each.
- **Gadi:** a full 104 ranks per node beat every reduced count. Gadi's Sapphire Rapids nodes have more memory bandwidth per core, so every core could be used.

**Why it was a turning point:** it overturned the belief the whole plan was built on. It also taught us that "what wins" depends on the machine, which turned our two-cluster study from duplicated effort into a source of contrasts to explain.

### 6. The 4-node bottleneck wasn't communication; it was the car's surface

Communication looked like the obvious 4-node problem. That impression came from CrayPat, HPE's profiler on ASPIRE 2A, which showed MPI time growing from 12% of each step at one node to 14% at two and 29% at four. Within that MPI time, `allReduce` dominated. allReduce is a collective in which every rank contributes a number and every rank waits for the combined result. Most of these calls come from the solver's coarsest multigrid level, which runs a fixed number of iterations per step whatever the node count.

That diagnosis predicted that MPI tuning would help, and it didn't. We tested nine MPI-side settings at two nodes: collective algorithms, transports, polling, rank reordering, and others. All nine tied the baseline. Nine ties in a row suggested the time inside allReduce wasn't the cost of communicating at all. It was the cost of waiting.

Waiting at a collective means some ranks arrive late, so we looked at which ranks were late. Per-rank correlation answered it. Scotch balances **cell counts** almost perfectly, but cells aren't equal. Ranks that held many **wall faces**, the faces on the car's surface where boundary conditions add extra work, were consistently slower. Those slow ranks made everyone else wait at the next allReduce, so imbalance showed up in the profile disguised as communication time. Wall-face count correlated with MPI wait time at r = −0.61: the ranks with the most surface waited least, because everyone else was waiting for them.

Waiting for them pointed to a fix, and the fix was out of reach. That fix would be a **weighted decomposition**, telling scotch to treat wall-adjacent cells as more expensive, so that surface-heavy ranks get fewer cells. We estimated a ceiling of about 5%. Our OpenFOAM build had no simple way to supply those weights, so it stayed future work.

**Why it was a turning point:** it corrected a conclusion already written into our documentation. It also became one of the questions we most expected the judges to ask, because it was the clearest gain we had left on the table.

### 7. Gadi's hidden variables: wall-clock time, stalls and node draws

The table above says Gadi was more forgiving about rank count. Gadi was less forgiving about almost everything else, and the first surprise was in the metric itself. The scored metric uses **wall-clock** time, not CPU time. Wall-clock time includes anything that makes the job wait, even when the processors are idle.

Idle processors showed up more often than we expected. On Gadi, occasional stalls in the shared Lustre filesystem added seconds to individual steps. Individual nodes also varied: one group of Sapphire Rapids nodes ran consistently slower than the rest, and node-to-node differences reached about 3%. Three percent is several times larger than some of the gains we were trying to measure.

Trying to measure through that kind of variance needed a different strategy. Our strategy became **submitting the best of several runs** of the final configuration, since the rules allowed it and the variance was outside our control. We also checked whether filesystem tuning could help, and it couldn't. Mesh reading at start-up is excluded from the score, and the solve phase writes almost nothing. So the stalls were a matter of luck, not a lever.

**Why it was a turning point:** it changed how we read every Gadi result. A rebuilt solver that looked no faster on average could still be faster, if it had drawn slower nodes. That problem set up the next turning point.

### 8. The Gadi rebuild: a tiny gain with a big lesson about FMA

Gadi's stock OpenFOAM was compiled for generic x86-64, so we rebuilt the solver for the actual hardware. The hardware is Sapphire Rapids, but Gadi's system GCC 8.5 doesn't recognise that target. That limitation pointed us to `-march=icelake-server`, which still enables the important instructions the generic build lacked: **FMA** (fused multiply-add) and AVX-512. Before the rebuild could even run, we had to work around missing build metadata in the stock install.

That rebuild was worth only 0.6–0.9% at four nodes. Such a small gain sat well inside Gadi's node-to-node variance, so raw averages of stock and rebuilt runs looked misleadingly equal. Equal-looking averages called for a controlled test: stock and rebuilt solvers run back to back on the same nodes inside one job, with hardware counters recording every pass.

Every pass told the same story. Executed instructions fell, but cycles didn't. Cycles stayed the same because the solver is memory-bound: it spends its time waiting for data, and fewer instructions don't make the data arrive sooner. What changed was a slightly higher clock speed, since the processor did less work per cycle while it waited. That clock increase was almost the entire gain. AVX-512 contributed close to nothing, because about 87% of the floating-point work is scalar. Most of it is in the Gauss–Seidel smoother, whose data dependencies stop it from being vectorised.

Those dependencies also explained something more worrying. FMA rounds once where a separate multiply and add round twice. Rounding once changes the last bits of each result, and in an iterative solver that small difference compounds. With FMA, Cd moved by 0.03% for scotch but 0.88% for hierarchical. A dedicated control build with FMA contraction switched off (`-ffp-contract=off`) confirmed that FMA alone caused both the speed gain and the Cd shift.

**Why it was a turning point:** it shaped the tier question. The rules put flags that change IEEE floating-point behaviour under Bonus, and FMA changes rounding. We eventually classified the rebuild as **Bonus**, which turned out to be the safer choice. It also left us with a precise answer for judges, "FMA, not vectorisation, and here is the proof", in place of a vague "compiler flags helped".

### 9. Both Bonus ideas came up empty, and Basic was locked

Locking Basic first was a rule, not a choice. That rule says Bonus speedups must be measured against the team's own Basic run, so our two Bonus ideas were tested against the configurations above.

The first idea targeted the allReduce calls from turning point 6. **GAMG processor agglomeration** gathers the coarsest multigrid level onto fewer ranks, so the global reductions happen among fewer participants. On ASPIRE 2A it passed the correctness check and cut allReduce calls by 82%. The 82% saving vanished in practice: the waiting simply moved to the next synchronisation point, because the underlying imbalance hadn't changed. On Gadi it was 3.2% slower, because funnelling coarse-level work onto one rank made the others wait for it.

The second idea was **multiLevel decomposition**, which splits the mesh first by node and then within each node. On ASPIRE 2A it tied on speed but failed the Bonus correctness check: Cd shifted 4.9% at four nodes, ten times outside the allowed ±0.5%. On Gadi we stopped it after a cheap decomposition-only check suggested it wouldn't beat scotch, saving most of a full run's budget.

That left the Basic results as our anchors:

| Cluster | Configuration | Result |
|---|---|---|
| ASPIRE 2A | scotch, 448 ranks, re-pinned | 2.92 s/step, 18.3% faster than the organisers' reference |
| Gadi | scotch, 416 ranks, FMA rebuild | 2.0538 s/step |

**Why it was a turning point:** it closed the "tune the configuration" phase of the competition. Everything after this point was about new code, better explanations, or presenting what we had honestly.

---

## Phase 2: Late wins and framing (late October to 6 November)

### 10. The pinning root cause was the kernel, not the MPI library

Our first explanation for turning point 4 blamed Cray MPICH. That explanation fit the evidence we had then: masks were correct before `MPI_Init` and wrong after it, so MPI looked responsible. It wasn't. A teammate's question about whether threads, not ranks, were being misplaced reopened the investigation. We followed it with `strace` and probe programs that recorded each rank's CPU mask and control group at several points during start-up.

Those records showed something no MPI setting could reach. The rank never called the system call that changes affinity. Instead, during the start-up handshake inside `MPI_Init`, the PBS scheduler moves each rank into the job's **cpuset control group (cgroup)**, the kernel mechanism that fences a job onto its allocated CPUs. Under cgroup v1, that move **resets the rank's CPU mask to the whole node**, silently undoing the launcher's correct binding.

Silently undoing it is why every MPI binding option we had tried had failed. Those options act before or during launch, and the reset happens afterwards, inside the kernel. So re-pinning after start-up, which is what `pin.sh` does, really was the right fix.

**Why it was a turning point:** the fix didn't change, but the story did, and the story is what judges score. "The scheduler's cgroup move resets affinity, so we re-pin after it" is precise, checkable, and doesn't wrongly blame a vendor library. We also built a plain-language version for a non-specialist audience: cooks who keep being shuffled away from their own stoves.

### 11. "Common baselines" changed how results were framed

The organisers introduced common baselines for scoring partway through. Those baselines mattered most for the Qwen task, where submissions didn't separate Basic from Bonus results. The team's decision was to lead with the Basic result (2,794.52 goodput, +52.5% over the baseline) and show the Bonus result (3,341.2, +82.4%) on top of it, rather than presenting the larger number alone.

That decision set the pattern for the whole deck. The pattern was: Basic first, Bonus measured against our own Basic, and both decomposition methods shown side by side on every OpenFOAM chart. Side-by-side charts cost us a cleaner headline, but they meant no judge could think we had hidden the method that lost.

**Why it was a turning point:** it made transparency the presentation strategy. That strategy paid off in turning point 13, when the tier labels had to be reconciled under time pressure.

### 12. A teammate's fused kernel became the late game-changer

The largest late gain came from new code. That code was a teammate's drop-in replacement for OpenFOAM's `smoothSolver::solve`. It **fuses the Gauss–Seidel sweep and the residual calculation into a single pass** over the matrix, where the stock code makes two. The solver is memory-bound, so a pass saved is memory traffic saved. The teammate estimated about 37% less traffic in that routine. The kernel loads at run time through `LD_PRELOAD`, so OpenFOAM itself is untouched.

Untouched source still needed proof of correctness, so the first job was checking that the change was legitimate. Legitimacy came down to one question: did it compute the same residuals the solver relies on, only in a different order? It did. We then built A/B infrastructure that ran baseline, fused, baseline, fused on the same nodes in one job, and used the kernel's own verify mode to compare every solve.

Every solve matched on ASPIRE 2A:

| Cluster | Speedup at 1, 2 and 4 nodes | Correctness |
|---|---|---|
| ASPIRE 2A | 9.5% to 12.0% faster | bit-identical Cd |
| Gadi (after fix) | 7.3% to 9.9% faster | verify mode: 0 mismatches |

That Gadi row hides a detour. On the first Gadi attempt, verify mode reported **20,800 mismatched solves out of 20,800**. Every mismatch traced back to one loop, and to the same FMA behaviour as turning point 8. ASPIRE's Cray GCC 11.2 and Gadi's GCC 8.5 rebuild contracted that loop's arithmetic into FMA instructions differently. So the fused and stock versions rounded differently on Gadi only. A one-line change, writing that operation explicitly as `std::fma`, made both compilers produce the same arithmetic. After it, verify mode found zero mismatches across 312,000 solves at the scored four-node configuration.

That configuration exposed one more Gadi quirk. Gadi runs weren't bit-reproducible even with *no* change, probably because MPI reductions combine numbers in different orders from run to run. On Gadi, then, correctness rested on verify mode plus Cd tolerance rather than comparing output files.

Output files and profiles together located the gain precisely. All of it came from the smoother calls for velocity and the two turbulence fields, about a third of each time step on both clusters. Within those calls, the speedup *grew* with node count: from 33% to 44% on ASPIRE 2A, and from 29% to 34% on Gadi, between one and four nodes. Why it grows remains unexplained.

**Why it was a turning point:** it was the only optimisation that carried across both clusters for a large gain, and it replaced the final numbers in our charts. It also produced our best story about teamwork. One person's idea was verified, debugged and ported by another, and a compiler difference that should have been a disaster turned into a one-line fix.

### 13. Reconciling the deck before the 3 November presentation

The final presentation was on 3 November. That deadline arrived while the deck still carried three weeks of evolving labels. Those labels contradicted each other in places. Some slides called the rebuild Basic and others Bonus. Rebuild gains were quoted with different figures, and one appendix slide showed Gadi data under an ASPIRE 2A title.

Titles were the easy part; the rules were the hard part. Rule F2 requires Bonus speedups to be measured against the team's own Basic run, so every Bonus number had to be re-anchored. Re-anchoring settled the rebuild question from turning point 8: it went to Bonus, with the stock Gadi build as the Basic reference. Two appendix slides explained FMA from scratch. They showed that FMA's effect on Cd was about 200 times smaller than the effect of switching decomposition method, and well inside the ±0.5% band.

That band gave us confidence in our answers, but not in every question. We prepared for the judges' most likely questions. The first was whether the fused kernel was valid. The second was why we hadn't fixed the surface-driven load imbalance. A third we could answer only honestly: why the fused kernel's gain grows with node count, which we didn't know.

**Why it was a turning point:** consistency became part of the result. A judge who catches one mislabelled slide starts doubting the rest, so a coherent deck protected numbers we had spent weeks earning.

### 14. Closing out the submission

Closing out the submission meant packaging every result so that someone else could check it. Checking required a specific layout: build files, job scripts, dictionaries, results by node count, and a README for each cluster. That layout didn't match how our files had grown, so both clusters' packages were rebuilt around it, with the originals kept as a fallback.

The fallback copies turned out to matter. Rebuilding the ASPIRE package exposed an old README that had labelled two runtime-only tests as Bonus. Under rule F1 those tests were Basic, and the new README corrected that. The final Read-me for the organisers then mapped every presented experiment to its job, script, log and Cd evidence. Where a slide's percentage didn't match the recomputed number, we removed the claim and wrote "no change beyond noise".

That wording was less impressive and more true. The OpenFOAM half was completed and checked against the shared folder the organisers received. The Qwen half went back to the Qwen team, the only people who could vouch for it. Everything was in before the 6 November noon deadline.

**Why it was a turning point:** it was the last chance to be wrong in public. Removing an unsupported number cost nothing, while leaving it in could have cost the credibility of everything around it.

### 15. Outcome: a Merit award and an ISC27 application

The outcome was a **Merit award** at the 9th APAC HPC-AI Competition. That award puts Team Kent Ridge in the tier just below the podium, among 33 finalists from 48 teams across 13 regions. Those teams will be recognised at SupercomputingAsia 2027 in Singapore.

Singapore is also where the next step starts. The next step is an application for the **ISC27 Student Cluster Competition**, whose candidate applications include ExaHyPE and ECsim. In that application, the stories we led with were the ones from this list: the cgroup pinning reset and the fused kernel.

**Why it was a turning point:** it turned a finished competition into a portfolio. The habits behind those two stories were profiling every change, repeating to measure noise and checking Cd before building on anything. Those habits carry over to new codes in a way that specific settings don't.

---

## The pattern behind the turning points

The turning points fall into two kinds. One kind overturned a belief: hierarchical wins (turning point 5), allReduce is the bottleneck (6), the MPI library breaks pinning (10). Each of those beliefs was reasonable when we held it. A reasonable belief that has never been measured is still just a guess, and on these machines the guesses were wrong more often than right.

The other kind came from diagnosis. Re-pinning (4) and the fused kernel (12) were worth roughly 7–12% each. Every MPI setting we tried was worth roughly nothing, and the compiler rebuild was worth under 1%. Under 1% is still worth knowing, but the lesson is about where to look. On a memory-bound solver, the largest wins come from finding out where time is *really* going: ranks fighting over cores, extra passes over memory, ranks waiting on a slow neighbour. Turning knobs on the parts that look slow comes a long way second.

Second place in that ranking also goes to the work that makes diagnosis possible. That work was measuring noise before tuning (2), keeping one loop across every cluster (3), and labelling results honestly when the rules got subtle (8, 11, 13, 14). None of it shows up as a speedup, and all of it is why the speedups were believable.

## Known issues and open items

- **The fused kernel's growing gain is unexplained.** Its smoother-only speedup rises from one node to four on both clusters. One hypothesis is that each rank's working set fits better in cache at higher node counts, which would make saved memory passes relatively more valuable. That hypothesis is untested.
- **Weighted decomposition was never tried.** The ~5% ceiling from turning point 6 is an estimate. Testing it first means confirming whether OpenFOAM's scotch interface can accept per-cell weights.
- **The superlinear-scaling explanation needs a hardware check.** We attributed better-than-linear scaling to per-sweep working sets becoming cache-resident. The actual L3 sizes on the nodes we ran on should be confirmed before relying on that.
- **Gadi energy data was collected but not analysed.** A run with per-second I/O, network and energy sampling is saved. The energy-per-step and DRAM-share numbers from it were never extracted.

## Next up

1. Finish the ISC27 application and size its hardware proposal around the candidate applications' real GPU support.
2. Read ExaHyPE 2 (built on the Peano framework) with the same loop: build cleanly, measure noise, profile, then change one thing.
3. Revisit the fused kernel's scaling behaviour, if cluster time becomes available, because an unexplained speedup is also an unexplained risk.

---

## Appendix: glossary quick reference

| Term | Meaning |
|---|---|
| Cell | One small 3D volume in the simulation mesh; this case has 65 million |
| Rank | One copy of the solver, owning one piece of the mesh and running on one core |
| Decomposition | Splitting the mesh into one piece per rank before a parallel run |
| `hierarchical` | A geometric decomposition that slices the mesh into boxes along x, y and z |
| `scotch` | A graph-based decomposition that cuts where the fewest faces cross between pieces |
| Processor face | A face shared by two ranks' pieces; its data is exchanged every iteration |
| Wall face | A face on the car's surface, where boundary conditions add extra work |
| RCM renumbering | Reordering cells so neighbours sit close together in memory |
| Memory-bound | Limited by how fast data reaches the processor, not by arithmetic speed |
| STREAM | A benchmark that measures a machine's achievable memory bandwidth |
| NUMA domain | A group of cores sharing one set of memory controllers |
| SMT | Simultaneous multithreading; each physical core appears as two logical CPUs |
| Pinning | Fixing which CPU each rank is allowed to run on |
| cgroup (cpuset) | The Linux kernel mechanism that fences a job onto its allocated CPUs |
| allReduce | An MPI collective where every rank contributes a value and waits for the combined result |
| GAMG | OpenFOAM's geometric-algebraic multigrid solver, which solves on coarser and coarser levels |
| Gauss–Seidel smoother | The routine that repeatedly refines the solution; most of the solver's floating-point work |
| Residual | A measure of how far the current solution is from satisfying the equations |
| FMA | Fused multiply-add: one instruction, rounded once, instead of a multiply and an add rounded twice |
| `LD_PRELOAD` | A way to load a replacement library at run time without changing the program |
| Cd | Drag coefficient; the correctness check for every run |
| Basic / Bonus | The competition's two tiers: settings and builds versus code and floating-point changes |
| s/step | Wall-clock seconds per solver iteration; the scored metric |
| Noise floor | How much an unchanged configuration varies purely from run to run |

## Appendix: numbers at a glance

| Turning point | Key number |
|---|---|
| 2. Shared nodes | ~16% lost to co-tenancy; 5–16% run-to-run variance |
| 4. Re-pinning (ASPIRE 2A) | 8.7% faster at 1 node, 7.2% at 4; noise 4.7% → 0.3% |
| 5. Scotch vs hierarchical | 40–50% fewer processor faces; 448 ranks beat 512 by 1.5% on ASPIRE 2A |
| 6. 4-node profile | MPI share 12% → 14% → 29%; nine MPI settings all tied; r = −0.61 |
| 7. Gadi variance | up to ~3% between nodes |
| 8. FMA rebuild (Gadi) | 0.6–0.9% faster; Cd shift 0.03% (scotch) vs 0.88% (hierarchical) |
| 9. Bonus attempts | agglomeration: 82% fewer allReduce calls, no gain (ASPIRE), 3.2% slower (Gadi); multiLevel: Cd off by 4.9% |
| 9. Basic anchors | ASPIRE 2A 2.92 s/step (18.3% over reference); Gadi 2.0538 s/step |
| 11. Qwen framing | Basic 2,794.52 (+52.5%); Bonus 3,341.2 (+82.4%) |
| 12. Fused kernel | 9.5–12.0% faster (ASPIRE 2A), 7.3–9.9% (Gadi); 20,800/20,800 mismatches → 0 |

---

*Setup: `occDrivAerStaticMesh`, OpenFOAM v2512, 65M cells. Scored work on NSCC ASPIRE 2A (2× AMD EPYC 7713 per node, PBS Pro, Cray MPICH over OFI, site OpenFOAM build) and NCI Gadi (Intel Sapphire Rapids `normalsr` nodes, 104 cores per node, PBS Pro, Open MPI, stock and `-march=icelake-server` builds). Practice work on NUS Vanda (Intel Xeon 8452Y) and the NUS School of Computing cluster.*
