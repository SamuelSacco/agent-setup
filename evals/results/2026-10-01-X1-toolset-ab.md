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

_(filled in after runs; protocol above is the pre-registration)_

## Verdict

_(pending)_
