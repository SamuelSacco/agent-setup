# X1 — Toolset A/B: full vs restricted toolset on real-code tasks

Date: 2026-10-01. Branch `lab/x1-toolset-ab` off master `ce0edbe`.
Backlog: `docs/experiments-backlog.md` X1. Spend cap: $1.50 metered,
hard stop at cap.

## Claim under test

The talk heuristic "≤ ~35 loaded tools per agent before splitting
into subagents" is UNVERIFIABLE folklore (no artifact ties 35 to an
outcome), and per-agent tool budgeting as an implementation was
REFUTED (X1a, `evals/results/2026-09-30-LAB-rent-toolcounts.md`):
both harnesses' defaults sit under 35 (Claude 12 tool defs, Copilot
23), so the rule is vacuously satisfied. This experiment does not
test the 35 threshold. It tests the outcome question underneath it:

**Does restricting an agent's usable toolset change task success on
real code, at the scale available here (full default vs a 6-tool
working set)?**

## Pre-registered protocol (written before any task run)

### Mechanism verification (probes, run before this protocol was
finalized; no task code involved, prompt = "Reply with exactly: OK")

Claude Code 2.1.285, model `claude-haiku-4-5-20251001`, raw API
bodies captured via `OTEL_LOG_RAW_API_BODIES` (method of ledger S8):

| Probe | Invocation | Tool defs in request body | Metered cost |
|-------|-----------|---------------------------|--------------|
| A | no `--tools`, no `--allowedTools` | 12: Agent, Bash, Edit, ListAgents, Read, ReportFindings, ScheduleWakeup, Skill, ToolSearch, Workflow, DeferredToolPlaceholder, Write | $0.015283 |
| B | `--allowedTools 'Read Write Edit Bash Grep Glob'` only | 14: the 12 above + Grep, Glob | $0.015380 |
| C | `--tools 'Read,Write,Edit,Bash,Grep,Glob'` + same `--allowedTools` | exactly 6: Bash, Edit, Glob, Grep, Read, Write | unmetered — client killed at 120 s after 3 request bodies were written, no response captured; $0.05 reserve held against the cap for it |

Finding from probes: `--allowedTools` alone does NOT restrict the
loaded toolset — it is a permission list, and naming Grep/Glob adds
their defs on top of the default 12 (14 loaded). The available-tools
allowlist is `--tools`: it restricts the loaded defs to exactly the
named set (probe C). Arm B therefore uses `--tools` + `--allowedTools`
with the identical 6-name list (the allowlist mechanism specified for
this experiment, applied in the form that disk-verifies as a
restriction). Probes A+B metered $0.030663; with the probe-C reserve,
$0.080663 of the $1.50 cap is committed before task runs, leaving
$1.419337.

### Arms

Same model (`claude-haiku-4-5-20251001`), same Claude Code 2.1.285,
same packaged prompt per task, same scratch setup, headless
`claude -p --output-format json --permission-mode acceptEdits`,
per-run `--max-budget-usd 0.40`, per-run wall cap 600 s.

- **Arm A — full:** no `--tools` flag (full default available set).
  `--allowedTools 'Agent Bash Edit Glob Grep ListAgents Read
  ReportFindings ScheduleWakeup Skill ToolSearch Workflow Write'`
  (13 names; pre-approval is required for headless use — ledger S6a).
  Loaded defs: 14 (default 12 + Grep + Glob, per probe B pattern).
  Usable: every loaded tool.
- **Arm B — restricted:** `--tools 'Read,Write,Edit,Bash,Grep,Glob'`
  + `--allowedTools 'Read Write Edit Bash Grep Glob'`. Loaded defs:
  exactly 6 (probe C). Usable: the same 6 — Read, Write, Edit, Bash,
  Grep, Glob. This is the plausible working set for a code-fix task
  and is ≤12 concrete tools. No other tools are added: filler tools
  would dilute the restriction, and the 6 suffice for every step of
  these tasks (read/search code, edit, run tests via Bash).
- Arm B's usable set is a strict subset of Arm A's. The only
  difference between arms is the toolset restriction.

### Tasks (4, mined by prior evals; no new mining)

Task packages are the oracle-validated packages in
`evals/tasks-packaged/` (mined for S11/S12 from real fix commits;
grading tests pass at the fix commit, fail at the parent with the
fix's test files overlaid — validation in
`evals/results/2026-09-30-P2-realcode-prereg.md` and the Rich
extension in `2026-09-30-P2-realcode-ab.md`).

Selection rule, fixed here before any X1 run: the 4 cheapest
packaged tasks by their prior published base-arm metered cost,
chosen so 8 runs fit the $1.50 cap. Prior base-arm costs:
nx-t2 $0.072, nx-t3 $0.075, rich-u1 $0.144, rich-u3 $0.203 — the
four cheapest of the eight packaged tasks (next cheapest is
rich-u2 at $0.269). Difficulty mix in prior base runs: t2 pass,
t3 pass, u1 pass, u3 fail.

| # | Package | Source | Parent → fix | Grading nodes |
|---|---------|--------|--------------|---------------|
| 1 | nx-t2-spanning-tree-iterator | networkx/networkx | `5d160909e` → `46a639aeb` | 1 (test_mst.py::TestSpanningTreeIterator::test_next_without_iter) |
| 2 | nx-t3-current-flow-closeness-small-graphs | networkx/networkx | `65becad79` → `fc87a81fd` | 1 node, 4 parametrized cases |
| 3 | rich-u1-pretty-dataclass-unset-field | Textualize/rich | `b6f2f7aa5` → `6055e2d8e` | 1 (tests/test_pretty.py::test_dataclass_no_attribute) |
| 4 | rich-u3-cells-zwj-width | Textualize/rich | `1d402e0c5` → `13f87a400` | 2 (tests/test_cells.py::test_zwj, ::test_non_printable) |

Prompts: each package's `prompt.txt` verbatim, with `{PYTHON}`
substituted by the grading interpreter — NetworkX:
`/home/hatch/workspace/p2/w3/scratch/venv/bin/python` (pytest 9.1.1,
numpy 2.5.3, scipy 1.18.1); Rich:
`/home/hatch/workspace/p2/secondcode/venv/bin/python` (pytest 9.1.1,
Pygments, markdown-it-py, attrs). Source clones (clean, contain
parent+fix): `/home/hatch/workspace/p2/w3/scratch/.infra/nx-src`,
`/home/hatch/workspace/p2/secondcode/.infra/rich-src`.

### Run and grading discipline

- Each run: parent commit exported via `git archive` into a fresh
  directory + fresh single-commit `git init` (no future history
  reachable) + `.claude/settings.json` with the Anthropic
  apiKeyHelper. Runs execute in pair order (task 1 A, 1 B, 2 A, …).
- Grading is by the evaluator after the agent exits, never from
  agent self-report: overlay the fix commit's test file(s) on the
  run tree, run the grading nodes with the task venv (Rich grading
  env adds `COLUMNS=200 TERM=dumb`, per the Rich prereg), success =
  every grading node passes.
- Per run recorded: pass/fail, `num_turns` and `total_cost_usd`
  from the Claude JSON envelope, wall seconds, `git diff --stat`.
- Raw per-run files follow the packaged runner's naming:
  `evals/results/2026-10-01-RUN-<task>-claude-<full|restricted>.md`.
- Stop rule: cumulative metered spend (probes' metered cost +
  probe-C reserve + task runs) is checked after every run; no new
  run starts if it would be launched past the cap. If the cap is
  hit mid-series, grade what exists and report partial n honestly.

### Decision rule (discordant-pair, as assigned)

- ≥1 discordant pair (arms differ on a task's pass/fail) → verdict
  PROVEN: toolset restriction at this scale changes outcomes.
- All 4 pairs concordant → verdict REFUTED-at-this-n (n=4 pairs):
  "toolset size at this scale affects success" does not reproduce;
  state n and the concordance explicitly. This does not test the
  35 threshold and does not generalize past these arms/tasks.
- Incomplete runs (cap, harness failure) → verdict scoped to the
  completed pairs, or UNVERIFIABLE if no pair completes.

## Results

### Delivered series (primary; complete envelopes, runner disk-grading)

| Task | Arm | Success | Turns | Cost USD | Wall s |
|------|-----|---------|-------|----------|--------|
| nx-t2 SpanningTreeIterator | full | **no** | 13 | 0.299612 | 139 |
| nx-t2 | restricted (6) | **yes** | 7 | 0.055467 | 148 |
| nx-t3 current_flow_closeness | full | — no result (ERROR, session terminated) | n/a | unmetered | n/a |
| nx-t3 | restricted (6) | **no** | 11 | 0.286612 | 205 |
| rich-u1 | both | not run — cap stop (below) | — | — | — |
| rich-u3 | both | not run — cap stop (below) | — | — | — |

Totals, delivered series: full = 0/1 graded, 13 turns, $0.299612.
Restricted = 1/2 graded, 18 turns, $0.342079. Completed pairs: 1
of 4 planned. Discordant pairs: **1** (nx-t2: full FAIL,
restricted PASS).

### On-disk duplicate series (incident; see below)

Every backgrounded launch executed a second time on this machine.
Those duplicate processes wrote to this filesystem, slowly and
incompletely; the evaluator killed the nx-t2-restricted and
nx-t3-restricted duplicates mid-run to stop duplicate billing
(their trees here are ungraded baselines and are not evidence).
The nx-t2-full duplicate ran to a graded result before the
divergence was understood:

| Task | Arm | Success | Turns | Cost | Wall s | Note |
|------|-----|---------|-------|------|--------|------|
| nx-t2 | full | **yes** | n/a (envelope lost) | unmetered | 600 (runner timeout) | Tree verified by evaluator: `mst.py` +3 lines, lazy `__iter__()` guard in `__next__` — a correct fix. File: `2026-10-01-RUN-nx-t2-spanning-tree-iterator-claude-full.md` (annotated). |

So the full arm on nx-t2 has two graded executions under the same
protocol: FAIL (delivered, clean exit) and PASS (duplicate, timeout
kill). The discordant pair that the decision rule fires on is
execution-dependent.

### Cost pattern (descriptive, n too small for a claim)

The restricted arm was cheaper on nx-t2 by 5.4× ($0.055 vs $0.300)
with half the turns, and solved it; on nx-t3 the restricted arm
cost $0.287 and failed (its full-arm pair never graded). Prior
S11/S12 base runs — which used the same 6-tool `--allowedTools`
set — cost $0.072 (nx-t2) and $0.075 (nx-t3); run-to-run cost
variance today was large in both arms.

### Spend accounting

Metered (JSON envelopes, exact): probes A+B $0.030663; task runs
$0.641691 (0.299612 + 0.055467 + 0.286612). **Metered total:
$0.672354 of the $1.50 cap.**
Unmetered (no envelope exists; estimates, not metered figures):
probe C (~3 API requests, no response captured, $0.05 reserve held
in the protocol); the duplicate executions (nx-t2-full ran a full
fix to completion; nx-t2-restricted, nx-t3-restricted, and the
nx-t3-full session were killed mid-run) — plausibly $0.15–0.45
combined at Haiku rates for the turns observed. Total billed is
therefore plausibly $0.87–1.17, under the cap on estimates but not
fully meter-verifiable. No further runs were launched once the
duplicate billing was identified: with nx-t3-full unmetered and
duplicates consuming unknown spend, launching the rich pairs
(projected $0.45–0.90 metered for 4 runs at today's prices) risked
breaching the cap. Stop rule applied; partial n reported.

## Incident: execution-layer duplication and filesystem divergence

Backgrounded shell launches in this environment executed each
command twice: a delivered execution (whose stdout, including the
runner's JSON, was returned to the evaluator) and an on-disk
execution on this machine (processes observable in `ps`, writing to
the workspace filesystem). Symptoms, all verified on disk: delivered
results arrived while the matching on-disk processes were still
running Claude with near-zero CPU; the delivered runs' result files,
ledger rows, and run-tree edits never appeared in this filesystem;
the on-disk nx-t2-full runner wrote its result file and ledger row
~10 minutes after launch, with a 600 s timeout and no envelope.
Foreground launches (probes A–C, all git/file operations) executed
once and persisted normally. Consequences: (1) duplicate API spend,
partly unmetered (above); (2) the delivered series' graded run trees
are not available for re-inspection — its per-run files in
`evals/results/` are evaluator reconstructions from the runner's
delivered JSON, labeled as such, except nx-t2-full, whose file is
the on-disk duplicate's own runner file, annotated; (3) killing the
on-disk duplicate of the combined nx-t3 session terminated that
session, losing the nx-t3-full delivered run (recorded as ERROR,
not a grade). This is an execution-layer failure, not an agent or
task failure; it is recorded here in full because it bounds what
this evidence can claim.

## Deviations from the protocol

1. Run order changed under the cap: nx-t3 ran before the rich
   tasks (pair order 1, 2, 4, 3 planned as cheapest-first
   completion), then the series stopped entirely (incident + cap).
   Rich pairs (rich-u1, rich-u3) were never launched.
2. Per-run files for the delivered series are reconstructions from
   runner JSON (incident above), not runner-written files.
3. Arm B used `--tools` in addition to `--allowedTools`, per the
   probe finding recorded in the protocol (planned, not a
   deviation in substance: `--allowedTools` alone disk-verifies as
   no restriction).

## Verdict

**Decision-rule outcome on completed pairs: PROVEN** — 1 completed
pair, 1 discordant pair (nx-t2: full FAIL / restricted PASS), which
meets the pre-registered ≥1-discordant-pair bar.

**Standing verdict: UNVERIFIABLE as a stable effect.** The single
discordant pair does not survive its own duplicate: a second
execution of the identical full arm on the identical task passed
with a correct fix, so at this evidence level the nx-t2 discordance
is attributable to run-to-run variance, not to the toolset. n=1
completed pair of 4 planned, one arm of nx-t3 ungraded, both rich
tasks unrun, and part of the spend unmetered (incident) — there is
no basis here to claim that restricting the toolset at this scale
(14 defs → 6) reliably changes success in either direction, and no
basis to refute it either: the restricted arm's nx-t3 failure has
no graded full-arm counterpart. The 35-tool threshold itself was
not tested (both arms sit under it) and remains UNVERIFIABLE
folklore; X1a's REFUTED (implementation) stands unchanged.

What this run does establish, descriptively: (a) `--tools`
restricts Claude Code's loaded tool defs to exactly the named set
(6/6, probe C) while `--allowedTools` alone does not (14 loaded,
probe B) — PROVEN by raw-body capture; (b) a 6-tool working set is
sufficient to solve a real NetworkX task end-to-end at the lowest
cost observed in this series ($0.055467, 7 turns).

