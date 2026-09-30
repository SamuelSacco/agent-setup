# P3 Big-Model Orientation A/B — Results

Date: 2026-09-30. Workstream E1. Pre-registration:
`evals/results/2026-09-30-P3-bigmodel-prereg.md` (committed + pushed
as 992b271 before run 1; Rich trigger addendum committed as e706f37
before the first Rich run). Raw per-run records:
`evals/results/2026-09-30-RUN-*.md`. Graded from disk only.

## Verdict

**UNVERIFIABLE at the top model tier, on both codebases.** On
`claude-opus-5-5` (Claude Code 2.1.285, `--model opus`), base and
+orientation solve the same tasks everywhere: NetworkX 3/4 vs 3/4,
Rich 3/4 vs 3/4 — zero discordant pairs in either direction across
8 pairs. Under the pre-registered S12 rule the orientation effect
does not reproduce at this tier. Mechanism, not mystery: the Haiku
discordant pair (T1) disappeared because Opus base solves T1 — the
headroom the orientation file exploited on Haiku is gone — and the
two remaining failures (T4, U3) are concordant, failed identically
by both arms on both tiers.

## Setup deltas vs the Haiku runs

- Model only. Same tasks, same prompts (verbatim assets; only the
  grading-interpreter path substituted), same orientation artifacts
  byte-identical (NetworkX sha256
  `ea8015523f0ec0142b891d27421b63dfbf70b1f275352bc58d87b2ef503d9515`;
  Rich sha256
  `35db19247ccdfab8c0583e20d64875ee62e0254927eea3791bcbd85e582e7f50`),
  same disk grading (real fix commit's tests overlaid, pinned
  venvs), executed through `scripts/run-eval.sh`.
- Exact model ID from run 1's JSON envelope: `claude-opus-5-5`
  (canonical, cost basis list). No checkout escapes: both mining
  source clones verified clean (`git status --porcelain` empty)
  before and after all runs; all agent changes are inside the
  per-run scratch trees.

## NetworkX (T1–T4) — Opus 5.5

| Task | Arm | Solved | Turns | Cost $ | Wall s | Grading |
|---|---|---|---|---|---|---|
| T1 ISMAGS empty candidates | base | yes | 9 | 0.189683 | 115 | 3 passed |
| T1 | +orientation | yes | 9 | 0.194882 | 158 | 3 passed |
| T2 SpanningTreeIterator next() | base | yes | 6 | 0.127089 | 73 | 1 passed |
| T2 | +orientation | yes | 5 | 0.122968 | 62 | 1 passed |
| T3 current_flow small graphs | base | yes | 4 | 0.099282 | 113 | 1 passed (4 cases) |
| T3 | +orientation | yes | 6 | 0.128524 | 160 | 1 passed (4 cases) |
| T4 stochastic_block_model sparse | base | **no** | 13 | 0.284851 | 199 | 2 failed |
| T4 | +orientation | **no** | 14 | 0.316735 | 148 | 2 failed |

Arm totals: base $0.700905, +orientation $0.763109. Set total
**$1.464014**. Per-set verdict: **UNVERIFIABLE** (equal totals, no
discordant pair).

Tier movement vs Haiku (same tasks): T1 base FAIL → PASS (the
discordant pair is erased from the base side); T4 PASS/PASS →
FAIL/FAIL (see failure notes).

## Rich (U1–U4) — Opus 5.5

| Task | Arm | Solved | Turns | Cost $ | Wall s | Grading |
|---|---|---|---|---|---|---|
| U1 pretty dataclass unset field | base | yes | 5 | 0.099218 | 31 | 1 passed |
| U1 | +orientation | yes | 5 | 0.108700 | 52 | 1 passed |
| U2 soft wrap styled text | base | yes | 12 | 0.217841 | 92 | 1 passed |
| U2 | +orientation | yes | 12 | 0.257723 | 87 | 1 passed |
| U3 cells ZWJ / non-printable | base | **no** | 8 | 0.178429 | 69 | 1 failed, 1 passed |
| U3 | +orientation | **no** | 15 | 0.316708 | 216 | 1 failed, 1 passed |
| U4 table padding width | base | yes | 16 | 0.259190 | 118 | 1 passed |
| U4 | +orientation | yes | 7 | 0.144723 | 56 | 1 passed |

Arm totals: base $0.754678, +orientation $0.827854. Set total
**$1.582532**. Per-set verdict: **UNVERIFIABLE** (equal totals, no
discordant pair) — same verdict as the Haiku Rich set.

## Discordant analysis

Discordant pairs: **none**, in either set, in either direction.
Every pair is concordant: six concordant passes, two concordant
failures (T4, U3). Pooled Opus n=8 pairs: base 6/8, orientation 6/8.
Pooled descriptively with Haiku (n=20 pairs): base 15/20,
orientation 17/20 — both discordant pairs in the pooled set are
Haiku/NetworkX pairs; no pooled verdict is claimed, the S12 combined
rule was pre-registered for the Haiku sets only.

## Failure notes

- **T4 (both Opus arms):** neither agent changed any library code.
  Both independently reported they could not reproduce the symptom:
  their density probes at the prompt's example parameters came out
  at/below p=0.25, and both concluded from the code that the
  diagonal branch never takes the sparse path. The oracle-validated
  grading tests (which pass at the real fix commit, fail at the
  parent — W3 validation) still fail. Recorded as observed: a
  stronger model trusted its own empirical check over the symptom
  report and stopped; the report's example parameters may
  under-specify the failing configuration, but grading follows the
  pre-registered oracle, not the agents' reasoning. Haiku's agents
  edited code and passed this task on both arms.
- **U3 (both Opus arms):** identical failure signature to Haiku —
  `test_zwj` fails with `assert 1 == 2`, `test_non_printable`
  passes. Orientation does not move this task at either tier.

## Cost notes (descriptive; no cost threshold was pre-registered)

- Orientation runs cost +8.9% (NetworkX) and +9.7% (Rich) over base —
  consistent with paying context rent for the orientation file when
  it buys no solves.
- Tier comparison, same 8 NetworkX runs: Opus total $1.464014 vs
  Haiku $2.132 (W3 batch 1). At list prices per token Opus is the
  expensive tier; per task it was cheaper here because it finished
  in far fewer turns (4–16 vs 7–43) and prompt-cache reads dominated
  the token mix.

## Spend vs cap

Total Anthropic spend, metered from run envelopes:
**$3.046546 of the $14.00 hard cap.** No runs were cut; the prereg
fallback rule never triggered (run 1: $0.189683). All 16 planned
runs (8 NetworkX + 8 Rich) completed — no timeouts, no harness
errors.

## Harness caveat

`scripts/run-eval.sh` names per-run files by date only
(`<date>-RUN-<id>-<tool>-<arm>.md`), so this stream's T2 base run
overwrote the S17 proof-run file of the same name in the working
tree. The proof run's original content is preserved in git history
(phase-2); the S17 verdict itself is unaffected (it cites the run,
whose record survives in history and in `docs/feedback-loop.md`).
Worth a timestamp in the runner's filename scheme; not changed here.
