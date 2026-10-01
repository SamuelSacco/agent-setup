# X10 — Specialist agent at higher n / harder band — Results

Date: 2026-10-01. Pre-registration: `evals/results/2026-10-01-X10-prereg.md`
(commit `138b9ba`, committed before any graded run). Claim under test:
ledger S11, "A specialist agent improves task success on real code vs
the base tool" — UNVERIFIABLE after the original test (2026-09-30, P2).

Codebase: networkx/networkx @ `92f497e2e` (same pin as the original).
Model for all runs: `claude-haiku-4-5-20251001`, Claude Code 2.1.285.
Success = every grading test from the real fix commit passes when
overlaid on the run tree and run by the evaluator (never agent
self-report).

## Outcome: 5 of 8 pairs completed; run truncated by API credit exhaustion

10 of 16 graded runs completed (5 complete pairs). The remaining 3
pairs (H8, H9, H10) were not run: after the H7 pair, every Claude
invocation returned `terminal_reason: api_error`, result text "Credit
balance is too low" (status 400) at $0 metered — the Anthropic account
credit was exhausted (the account is shared across workstreams; X10's
own metered spend was $3.98 of its $5.00 cap). Two H8-base attempts hit
this and are recorded as invalid/unrun, not as failures. Per the
pre-registration, the decision rule is applied to completed pairs
only and unrun tasks are marked unrun — never graded, never imputed.

## Per-task pair table (completed pairs)

| Task | Base | Agent (backend) | Base turns / cost | Agent turns / cost | Grading tests |
|------|------|-----------------|-------------------|--------------------|---------------|
| H1 vf2 isolated-node iterators | **yes** | no | 40 / $0.442 | 40 / $0.459 | base 40 passed; agent 6 failed, 34 passed |
| H3 directed node connectivity/cuts | no | no | 31 / $0.297 | 61 / $0.552 | both 5 passed, 5 failed |
| H4 k_components | no | no | 63 / $0.854* | 37 / $0.373 | both 3 passed, 1 failed |
| H6 edge-betweenness k<N | **yes** | **yes** | 19 / $0.210 | 24 / $0.288 | both 2 passed |
| H7 is_aperiodic edge cases | **yes** | no | 25 / $0.273 | 19 / $0.235 | base 4 passed; agent 3 passed, 1 failed |
| H8 PlanarEmbedding.to_undirected | unrun | unrun | — | — | API credit exhausted |
| H9 weakref cached views | unrun | unrun | — | — | API credit exhausted |
| H10 WL hashing directed + iterations | unrun | unrun | — | — | API credit exhausted |

\* H4 base cost reconstructed from the session-jsonl usage records
(envelope lost; see Deviations). Reconstruction method validated
against H3 agent, whose envelope survived: reconstructed $0.5522 vs
envelope $0.5522325.

## Totals (completed pairs, n=5 tasks per arm)

| Arm | Solved | Turns | Cost USD | Mean cost/run |
|-----|--------|-------|----------|---------------|
| base | 3/5 | 178 | $1.222 + $0.854 (H4 recon.) = $2.076 | $0.415 |
| +agent (backend) | 1/5 | 181 | $1.908 | $0.382 |

**Total metered spend: $3.98 of the $5.00 cap** (10 graded runs;
the 2 invalid H8 attempts metered $0).

## Verdict (pre-registered rule)

Discordant pairs: specialist-only solves **0** (none); base-only
solves **2** (H1, H7). Net discordant = 0 − 2 = **−2**.

- PROVEN requires net ≥ +2 — not met.
- **REFUTED: net discordant ≤ −2 — met.** Ledger S11 is amended to
  REFUTED (2026-10-01) in this same commit series.

Scope of the verdict, stated plainly: the rule fires on the 5
completed pairs. The 3 unrun pairs cannot be assumed either way; had
they run and all favored the specialist, the net could have reached
+1, still short of PROVEN, but above the REFUTED line. The REFUTED
verdict is therefore a verdict on the completed evidence under the
pre-registered rule, with truncation caused by an external credit
exhaustion, not by the budget rule. The descriptive record is
one-directional in the completed pairs: the specialist solved fewer
tasks (1/5 vs 3/5), produced zero discordant wins, and its two
discordant losses were outright regressions on tasks base solved.

Cost pattern differs from the original: the specialist was not the
expensive arm here (mean $0.382 vs base $0.415; turns 181 vs 178,
+1.7%). The base mean is driven by H4 base's $0.854 outlier; medians
are base $0.297, agent $0.373. No cost claim is registered either way
at n=5.

## Comparison against the original S11 test (2026-09-30, P2)

| | Original (n=4, easy band) | X10 (n=5 completed, harder band) |
|---|---|---|
| Base solves | 3/4 | 3/5 |
| Specialist solves | 3/4 | 1/5 |
| Discordant pairs | 0 either way | 2, both favor base |
| Specialist turns delta | +55% | +1.7% |
| Specialist cost delta | +8.5% | −8.1% (mean; medians reverse) |
| Verdict | UNVERIFIABLE | **REFUTED** (rule on completed pairs) |

The harder band did what it was designed to do: it created headroom
(base fell from 3/4 to 3/5 with two concordant failures) — and the
specialist took none of it. On the two tasks where the arms separated
at all, base won both.

## Failure notes

- **H1 × agent — partial vf2 fix.** Agent changed `isomorphvf2.py`
  (12+/8−) and fixed the reuse/mapping behavior, but
  `test_isomorphism_iter3` still fails in both parametrizations
  (6 failed, 34 passed): the isolated-node subgraph iterators remain
  empty. Base's larger rewrite (20+/9−) passes all 40.
- **H3 × both — identical miss.** Both arms fail the same 5 of 10
  nodes, all in `test_cuts.py` directed minimum-node-cut cases
  (`not_strongly_connected`, `both_orders` families); both pass the
  connectivity-side nodes. Agent spent 61 turns / $0.552 vs base 31 /
  $0.297 for the identical grade signature.
- **H4 × both — partition node survives.** Both arms fail exactly
  `test_generate_partition_does_not_drop_cutset_nodes` (3/4 pass).
- **H7 × agent — one case short.** Agent passes 3/4; it does not raise
  on the weakly-connected digraph (`test_is_aperiodic_weakly_connected_raises`).
  Base passes 4/4.
- **H6 × both — pass.** Both arms make the same 1-line rescale fix.

## Deviations and incidents (complete list)

1. **Truncation by API credit exhaustion** (above): H8/H9/H10 unrun.
   The $5.00 cap was not reached ($3.98 metered). The preregistered
   rule was applied to completed pairs only, per the prereg.
2. **H4 base envelope lost.** The launching exec session was SIGTERM'd
   at ~557 s by the runtime; the Claude child completed orphaned and
   its tree was graded from disk as normal. Cost/turns reconstructed
   from the session jsonl (deduplicated by message id; Haiku 4.5 list
   prices), validated to $0.0001 against a surviving envelope (H3
   agent). Wall time for that run is not recorded (marked
   `orphan-see-note` in the ledger).
3. **Runner SHA typo caught before any H7 run:** the runner's H7
   parent SHA was mistyped at setup; the first H7-base launch failed
   at `git archive` ($0, no agent run). All 8 tasks' commit/parent
   SHAs were then re-verified against `git rev-parse <commit>^` and
   the mining table before relaunching. No graded run was affected.
4. Screening/validation cost $0 (no agent runs), as pre-registered.
   Two of 10 mined candidates were dropped at oracle validation
   (pandas-gated test file; new-API-symbol task) — recorded in the
   prereg.

Artifacts: `~/workspace/q2-x10-scratch/` (`runner.py`, `assets/`
prompts + emitted `backend.md`, `runs/` trees + raw envelopes,
`ledger.tsv`); mining/validation in `~/workspace/x10-scratch/`
(`tasks.json`, `validation.json`, `validate.py`).
