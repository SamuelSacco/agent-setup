# S25 — Self-review behavior probe, rerun after skill fix

Date: 2026-10-01. Branch: `feat/soul-self-review` at `e724470` (run 1 was at
`7220a9f`). Clone: `~/workspace/w2-rerun`, local clone of `~/workspace/w2-soul`;
`./scripts/install.sh` exit 0.

## Why a rerun

Run 1 (see `2026-10-01-S25-self-review-behavior-probe.md`) graded PARTIAL:
protocol mechanics fired (routing, persona bar, 5-axis entry, wiki log,
`self-review:` commit), but the AGENTS.md lessons were generic — the seeded
durable fact (test suite lives in `demo/`) was dropped — and lessons cited no
session file. Fix landed in `e724470`: `self-review` skill gained a mechanism
rule (a lesson must name the concrete command/directory/setting that prevents
recurrence; a session's `## Learned` fact must be routed with its mechanism
intact) and a pre-commit conformance checklist (dated, mechanism named, exact
session-file path citation per lesson); AGENTS.md §8 Lessons format comment
updated to match.

## Run details

- Fixture identical to run 1: seeded session
  `wiki/sessions/2026-10-01-0900-claude-code-seeded-task.md` (3 identical
  root-level test runs, 'no tests collected', Learned = `demo/` fact), one
  sidecar `record-session-end` hint. Baselines matched run 1 exactly:
  SOUL.md md5 `9bfb0420dad8982559fae9e4e6d87110`, wiki/log.md md5
  `7c25cbd78eb57af4e10f5007419bef7d`.
- Auth: `.claude/settings.local.json` apiKeyHelper (same as run 1). Binary
  `~/workspace/tools/bin/claude` (2.1.285), model `claude-haiku-4-5-20251001`.
- Command: `claude -p "Close out the work: the seeded session from this
  morning is finished. Run the self-review skill now and complete every step
  it requires." --output-format json --permission-mode acceptEdits
  --allowedTools "Read Write Edit Bash Grep Glob"` (timeout 900).
- Result: exit 0, JSON envelope present (run 1's timeout kill did not
  recur). Cost $0.12317205, 17 turns, `is_error: false`.

## Verdicts (graded on disk only, run-1 rubric)

### 1. Right file — PASS
Two dated lessons appended to AGENTS.md §8 Lessons (from `git show c35a5a5`):

- "Every discovered fact in `## Learned` must carry a verdict: prefix with
  **PROVEN**, **REFUTED**, or **UNVERIFIABLE**. Example: "**PROVEN** — The
  eval suite location is demo/; running pytest from repo root collects zero
  tests." … (wiki/sessions/2026-10-01-0900-claude-code-seeded-task.md)"
- "Session outcome must end with concrete next steps, naming the exact
  command, directory, or file path … "Run `python -m pytest` from demo/ to
  see the failure; then examine demo/parser.py to implement the fix." …
  (wiki/sessions/2026-10-01-0900-claude-code-seeded-task.md)"

The seeded working-directory fact is encoded with its mechanism in both.
1B: SOUL.md md5 identical before/after (`9bfb0420…`) — persona bar held.

### 2. Dated + evidence-cited — PASS
Both lessons dated 2026-10-01 and end with the exact session-file path in
parentheses — the run-1 citation failure is fixed.

### 3. 5-axis entry — PASS
Appended to the seeded session file: Accuracy 5, Completeness 3, Clarity 3,
Actionability 2, Evidence discipline 2 — each with a cited instance from the
seeded session. Axes ≤ 2 routed to lessons per skill step 2.

### 4. Wiki log — PASS
Exactly one line appended (commit diff: +1), naming ratings, lessons, and
the session file.

### 5. Committed — PASS
`c35a5a5 self-review: 2026-10-01` — label exact; AGENTS.md, wiki/log.md, and
the seeded session file in one commit.

## Overall verdict: PROVEN

5/5 criteria on rerun, against run 1's PARTIAL on identical fixture and
rubric. The delta is the skill fix (mechanism rule + conformance checklist),
not the model or the fixture. Scope: Claude Code, Haiku 4.5, n=1 per arm —
the pattern is proven workable, not proven robust across models or repeated
weeks. Copilot behavior under this protocol remains untested (its cadence is
manual per AGENTS.md §8; SessionEnd delivery UNVERIFIABLE, ledger S4/S19).

Spend: run 1 $0.0992 + rerun $0.1232 = $0.2224 (behavior probe total).
