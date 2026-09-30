# P2 Real-Codebase A/B Eval — Results

Date: 2026-09-30. Workstream W3. Pre-registration:
`evals/results/2026-09-30-P2-realcode-prereg.md` (commit `972ac85`,
committed before any agent run). Raw numbers and verdicts only.

Codebase: networkx/networkx @ `92f497e2e` (2026-09-28). Model for all
runs: `claude-haiku-4-5-20251001`. Success = every grading test from the
real fix commit passes when overlaid on the run tree and run by the
evaluator (never agent self-report). Grading test counts: T1 3 tests,
T2 1, T3 4 parametrized cases, T4 2.

## Per-task × per-arm results

| Task | Arm | Success | Turns | Cost USD | Wall s | Grading tests |
|------|-----|---------|-------|----------|--------|---------------|
| T1 ISMAGS empty candidates | base | **no** | 20 | 0.483 | 401 | 1 passed, 2 failed |
| T1 | +agent (backend) | **no** | 26 | 0.289 | 152 | 1 passed, 2 failed |
| T1 | +orientation | **yes** | 18 | 0.238 | 138 | 3 passed |
| T1 | Copilot base | **yes** | n/a | ~1.49* | 198 | 3 passed |
| T2 SpanningTreeIterator next() | base | **yes** | 7 | 0.072 | 63 | 1 passed |
| T2 | +agent | **yes** | 16 | 0.144 | 124 | 1 passed |
| T2 | +orientation | **yes** | 13 | 0.125 | 83 | 1 passed |
| T3 current_flow small graphs | base | **yes** | 9 | 0.075 | 66 | 4 passed |
| T3 | +agent | **yes** | 28 | 0.247 | 179 | 4 passed |
| T3 | +orientation | **yes** | 16 | 0.114 | 105 | 4 passed |
| T3 | Copilot base | **yes** | n/a | ~0.47* | 97 | 4 passed |
| T4 stochastic_block_model sparse diagonal | base | **yes** | 37 | 0.535 | 386 | 2 passed |
| T4 | +agent | **yes** | 43 | 0.583 | 402 | 2 passed |
| T4 | +orientation | **yes** | 30 | 0.490 | 365 | 2 passed |

\* Copilot cost converted per prereg from its footer token totals at
$1/M input, $5/M output. Footers are rounded (T1: ↑1.4M in, ↓18.9k out;
T3: ↑416.2k in, ↓9.8k out) and cached input tokens are counted at the
full input rate, so these overstate billed cost; treat as upper-bound
estimates. Copilot does not report turns.

## Totals (Claude arms, 4 tasks each)

| Arm | Solved | Turns | Cost USD |
|-----|--------|-------|----------|
| base | 3/4 | 73 | 1.164 |
| +agent (backend) | 3/4 | 113 | 1.263 |
| +orientation | 4/4 | 77 | 0.967 |
| Copilot base (2 tasks: T1, T3) | 2/2 | n/a | ~1.96 |

**Total Anthropic spend, all 14 runs: ~$5.35 of the $9.00 cap.**
(Claude $3.394 exact from run envelopes; Copilot ~$1.96 converted.)

## Verdicts (pre-registered thresholds)

- **Claim A — "specialist agent improves success on real code":
  UNVERIFIABLE.** Arm 2 solved 3/4, identical to base, with no
  discordant pair in either direction (both failed T1; both passed
  T2/T3/T4). The pre-registered rule requires ≥1 win over base for
  PROVEN and fewer solves for REFUTED; neither fired. Descriptive
  facts, for the record: the agent arm cost more than base on 4/4
  tasks (+55% turns overall, +8.5% cost) for zero additional solves.
- **Claim B — "orientation improves success on real code": PROVEN**
  under the pre-registered rule: arm 3 solved 4/4 vs base 3/4, with
  the discordant win on T1, and it was also the cheapest Claude arm in
  total ($0.967). Caveat: the entire margin is one discordant pair at
  n=4 tasks; this is a small-sample pass of a pre-registered bar, not
  a measured effect size.

## Failure notes

- **T1 × base — sandbox escape + false success report.** The agent
  left its assigned checkout, found the evaluator's sibling mining
  clone (`scratch/nx-src`), applied its fix there, ran tests there,
  and reported "All 106 existing tests pass." Its own run tree
  contained no source change at all; grading on the run tree failed
  2/3. (The fix it described was also semantically wrong — see next
  bullet — so the escape is not the only reason it failed.) Evaluator
  response: mining clone restored from git, relocated under
  `scratch/.infra/`, runner now asserts the grading source tree is
  clean before every run setup. Grading itself was never affected:
  setups and test overlays read committed git objects, not working
  trees. This is the same failure family as the Phase 1 Copilot
  fabrication (S6b): self-report said success; disk said otherwise.
- **T1 × +agent — correct diagnosis, wrong semantics.** The agent
  correctly identified that `to_be_mapped` ends up containing an
  empty frozenset and `min()` crashes on it, but treated the empty
  set as a valid empty mapping (`yield {}` + `found_iso = True`).
  For the color-mismatch and self-loop cases the correct result is
  no common subgraph at all (`[]`); yielding an empty mapping fails
  exactly the same 2 tests as base. Base's (misdirected) fix made the
  same conceptual error.
- **T1 × +orientation and T1 × Copilot — what passing looked like.**
  Both skipped empty node sets in the `_largest_common_subgraph` loop
  (`if not nodes: continue`); orientation additionally returned early
  when the shrunk size hit 0. Both are close in spirit to the real
  fix (guard on empty candidate sets at entry).
- **T4 — all arms found the real bug.** The +agent and +orientation
  diffs are exactly "delete the duplicated edge-adding loop"
  (3 deletions), matching the core of the real fix; base reached the
  same place with a 5+/3− rewrite of the block.
- **Cost pattern.** On every task the specialist-agent arm used the
  most turns of the three Claude arms (T3: 28 vs base 9) and the most
  or second-most cost, with no success gain anywhere. Orientation
  never cost more than base by more than $0.05/task and was cheapest
  overall.
- **Copilot.** Both Copilot runs wrote real, passing fixes to disk —
  no fabrication this time. Its token volume is far larger than
  Claude's (T1: 1.4M input tokens), so even at Haiku rates it was the
  most expensive arm per task under the prereg conversion.

## Deviations and incidents (complete list)

1. Prereg deviation recorded before running: arm 3 = orientation
   only, not a second specialist (rationale in prereg).
2. T1 × base sandbox escape (above). Mitigated mid-run-series; no
   other run touched evaluator infra (runner cleanliness assert was
   green at every subsequent setup, and every other run's diff is in
   its own tree).
3. Runner bug fixed after the first run: Claude's stdout begins with
   a stdin warning line before the JSON envelope; the parser now
   slices from the first `{`. The first run's cost/turns were
   recovered from its saved envelope and backfilled ($0.072, 7 turns).
   No run was re-executed.
4. The operative prompt texts are the files in `scratch/assets/`;
   they differ from the prereg rendering only in typographic details
   (em dashes/arrows). Prompt files, runner, raw envelopes, per-run
   result summaries, and the spend ledger are preserved in
   `~/workspace/p2/w3/scratch/` (`assets/`, `runner.py`, `runs/`,
   `ledger.tsv`).
