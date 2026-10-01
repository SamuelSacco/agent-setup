# X9 / E6 re-run — Claude arm — PRE-REGISTRATION — 2026-10-01 00:35 ET

Registered before any paid CLI run on this arm. Branch
`wave2c/x9-e6-claude-arm` off master `e181f61`.

## What is being re-run

The E6 protocol as actually executed on 2026-09-30 (pilot +
`2026-09-30-E6-rerun-claude.md` + `2026-09-30-S6B-preapproved-rerun.md`):
one bounded task, canonical `backend` agent, both tools, fresh repo copy
with adapters installed. The full 3-agent × 3-task blind grid in
`evals/tasks/E6-agent-parity.md` was never run and its 3 matched tasks
were never specified, so it cannot be re-run unchanged; the executed
task package below is the only re-runnable E6 protocol. This worker runs
the Claude arm only; a counterpart worker runs the Copilot arm on a
separate branch for comparison.

## The one change vs the original runs

Grading is from disk artifacts only. Agent self-report (test counts,
summaries) is recorded but never used as evidence. This matches how
S6a/S6b were in fact graded (independent pytest re-run); X9 makes it the
stated rule and adds a grader-written contract probe + a disk rubric
score so the two arms can be compared numerically.

## Protocol (fixed)

- Fixture: fresh copy of this repo @ `e181f61` in
  `~/workspace/w2c-x9-scratch/e6-claude-x9/`, `./scripts/install.sh` run
  (emits `.claude/agents/backend.md`). Pre-run file snapshot taken;
  `ratelimit.py` / `test_ratelimit.py` must be absent before the run.
- Tool: Claude Code 2.1.285 (`~/workspace/tools/bin/claude`).
- Model: `claude-haiku-4-5-20251001` (`--model haiku`) — same model as
  pilot, S6a rerun, and S6b rerun.
- Auth: stored Anthropic credential via `apiKeyHelper` surrogate
  (`--settings`), same path as the prior runs. No raw key handled.
- Permission mode (pre-approved writes, as S6a): `--permission-mode
  acceptEdits` + `--allowedTools Write Edit Bash Read`.
  `--dangerously-skip-permissions` is refused under root (recorded
  2026-09-30); not retried.
- Invocation: `claude -p "$PROMPT" --agent backend --model haiku
  --output-format json`, cwd = fixture root.
- Prompt (verbatim, identical to the S6b rerun's recorded prompt):
  "State a contract first. Then implement a TokenBucket rate limiter in
  ratelimit.py in the current directory: TokenBucket(capacity,
  refill_per_sec) with an allow(tokens=1.0) method that returns True and
  consumes the tokens when enough are available, and False otherwise;
  the bucket refills over time up to capacity. Write pytest tests in
  test_ratelimit.py covering: burst up to capacity, denial when the
  bucket is empty, and refill over time. Run the tests with pytest and
  report the results."
- One run only. No retry on a poor result; a harness error (no JSON
  envelope, non-zero exit before any model turn) may be re-run once and
  both attempts recorded.
- Spend cap: $1 metered for this arm. Abort if the single run's metered
  cost would exceed it (it cannot be known mid-run; the cap binds any
  further runs).

## Disk grading (fixed)

1. Tree diff vs pre-run snapshot: which files were added/changed.
2. `ratelimit.py` / `test_ratelimit.py`: existence, byte size, md5.
3. Independent re-run of the agent's tests in a fresh venv
   (pytest): pass/fail counts and exit code are the grade.
4. Grader-written contract probe (positional args only, so parameter
   naming is not graded): burst to capacity → True; next allow on empty
   → False; refill after a sleep at a known rate → True; rate 0 → no
   refill. Probe pass/fail recorded per case.
5. Rubric score /10 from disk artifacts only, per `E6-agent-parity.md`
   axes: correctness (probe + independent pytest, 0–4), test presence
   and coverage of the 3 named cases (0–3), convention fit (contract
   stated in the run output, files/names as specified, 0–2), clarity
   (docstrings/readable structure in the files on disk, 0–1).
6. Metered cost and turns from the run's JSON envelope
   (`total_cost_usd`, `num_turns`), cross-checked against the files.

## Verdict rule

- Claude arm verdict: PROVEN if both files exist on disk, the
  independent pytest re-run passes, and the contract probe passes all
  cases. REFUTED if the run completes and any of those fail. UNVERIFIABLE
  if the run cannot execute (harness/auth failure).
- S6 parity itself is decided by the coordinator when both arms exist:
  PASS per `E6-agent-parity.md` if the two arms' rubric scores differ by
  ≤ 1 point. This file makes no parity claim alone.
