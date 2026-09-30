# P3 Big-Model Orientation A/B — Pre-Registration

Written and committed BEFORE any agent eval run in this workstream.
Date: 2026-09-30. Workstream E1 (Phase 3 extension of the P2 real-code
A/B). Raw data deliverable; no presentation framing.

## Question

Does the orientation effect survive a model-tier change? All prior
orientation evidence is Haiku 4.5: NetworkX combined 8/8 vs base 6/8
(ledger S12, PROVEN at the pre-registered bar), Rich 3/4 vs 3/4
(UNVERIFIABLE there). Two published nulls (ETH Zurich/LogicStar;
Khatri) used frontier-model setups. This stream re-runs the identical
protocol on a top-tier model and applies the identical decision rule.

## Tool and model

- Claude Code **2.1.285** (`~/workspace/tools/bin/claude --version`,
  recorded 2026-09-30 before runs).
- Model: `--model opus` (CLI alias), passed via
  `scripts/run-eval.sh --model opus`. The exact model ID the CLI
  reports (JSON envelope `modelUsage`) will be transcribed into the
  results file from run 1's raw envelope before further interpretation.
- Auth: `.claude/settings.json` apiKeyHelper, same as W3 (Anthropic
  API key; Samuel topped the key up 2026-09-30 14:24 ET).

## Arms

Identical to W3 arms 1 and 3, executed through the packaged runner
(`scripts/run-eval.sh`, mechanics equivalent to the W3 runner: parent
commit exported via `git archive` into a fresh single-commit tree,
headless `claude -p`, `--permission-mode acceptEdits`,
`--allowedTools Write Edit Bash Read Glob Grep`, per-run wall cap
900 s):

- **base:** scratch checkout + apiKeyHelper settings only.
- **+orientation:** scratch checkout + `CLAUDE.md` at the checkout
  root containing the frozen W3 orientation text, byte-identical to
  the artifact used in the Haiku runs:
  `evals/fixtures/networkx-orientation.md`,
  sha256 `ea8015523f0ec0142b891d27421b63dfbf70b1f275352bc58d87b2ef503d9515`
  (copied read-only from the W3 assets; hash verified at copy time).

## Tasks

NetworkX tasks from the W3 fixtures, prompts verbatim (asset files;
the only substitution is the grading-interpreter path via the
runner's `{PYTHON}` placeholder, resolved to the same pinned W3 venv:
Python 3.12, pytest 9.1.1, numpy 2.5.3, scipy 1.18.1). Parent/fix
commits, grading test files and node IDs are in each task package
(`evals/tasks-packaged/nx-t*/task.json`) and match the W3
pre-registration exactly. All four tasks were oracle-validated in W3
(grading tests pass at the fix commit, fail at the parent).

Run order — complete each task's pair before starting the next task:

1. **T1** ISMAGS empty candidates (`nx-t1-ismags-empty-candidates`) —
   the Haiku discordant pair (base failed, +orientation passed) and
   the task where Haiku base escaped its checkout.
2. **T3** current_flow_closeness small graphs
   (`nx-t3-current-flow-closeness-small-graphs`) — cheapest Haiku task.
3. **T2** SpanningTreeIterator (`nx-t2-spanning-tree-iterator`,
   existing package).
4. **T4** stochastic_block_model sparse diagonal
   (`nx-t4-stochastic-block-model-sparse-diagonal`) — most expensive
   Haiku task; first in the cut order.

**Rich U1–U4** (fixtures in `evals/tasks-packaged/` to be created
from the second-codebase fixtures, Rich orientation artifact
`evals/fixtures/rich-orientation.md`, sha256
`35db19247ccdfab8c0583e20d64875ee62e0254927eea3791bcbd85e582e7f50`)
run ONLY if all 8 NetworkX runs complete AND the projection rule
below leaves the full Rich set (8 runs) inside the cap. Rich grading
environment deviation, pre-noted: the second-codebase runner graded
with `COLUMNS=200 TERM=dumb`; if Rich runs happen, the same env vars
will be set for the runner invocation and recorded.

## Decision rule (identical to S12)

Per codebase set, applied to completed pairs:

- **PROVEN** — orientation solves more tasks than base, with ≥1
  discordant win (orientation passes a task base fails) and no
  discordant loss.
- **REFUTED** — base solves more tasks than orientation.
- **UNVERIFIABLE** — otherwise (equal totals with no discordant pair,
  or incomplete pairs).

The NetworkX set is the primary verdict. n will be small; the verdict
is reported with its n and per-task table, never as a powered claim.

## Budget and cost discipline — $14.00 HARD CAP

- Meter: `total_cost_usd` from each run's Claude JSON envelope, as
  recorded in the runner's per-run results file. Cumulative spend is
  logged in the results file after every run.
- **No run is launched if it would put projected cumulative spend
  over $14.00.**
- Run 1 (T1 base) is the calibration run. After each completed run,
  project: `projection = spent + 1.25 × (mean cost of completed
  runs) × (runs remaining in the current plan)`.
- **Cut rule:** if the projection for the remaining plan exceeds
  $14.00, drop the lowest-priority remaining task pair (cut order:
  T4, then T2, then T3) and record the cut in an addendum to this
  file, committed BEFORE running the reduced set. Repeat as needed.
- **Fallback rule:** if run 1 costs > $3.50, even a minimal Opus set
  (T1 pair + one more pair) projects over the cap. Then: complete
  the T1 pair on Opus only if the pair projection stays ≤ $7.00;
  otherwise stop Opus after run 1. The remaining NetworkX tasks
  (T3, T2, T4 in that order) then run on the strongest Sonnet tier
  (`--model sonnet`) as a separately-verdicted set. The fallback and
  the exact Sonnet model ID are recorded in an addendum to this file
  BEFORE any Sonnet run launches.
- Single-run guard: a run whose cost is still accruing is bounded by
  the 900 s wall cap; if a single run's envelope cost exceeds $4.00,
  treat the next projection with that run weighted double (the 1.25
  factor already applies; no further runs launch until the addendum
  re-plans the set).

## Grading

By the packaged runner, from disk only, never from agent self-report:
the real fix commit's test files are overlaid onto the run tree and
the grading nodes executed with the pinned venv; PASS = every
grading node passes. Per run recorded: verdict, turns, envelope cost,
wall seconds, `git diff --stat`, and checkout-escape check (any
modification outside the run tree — mining source clones are opened
read-only and verified clean before/after).

## Relationship to S12

S12's Haiku verdict is untouched. Whatever this stream finds is
recorded as a model-tier scope note (new ledger claim or S12
amendment — decided at write-up, justified there).
