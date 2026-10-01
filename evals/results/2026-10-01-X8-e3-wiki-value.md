# X8 / E3 — Does the wiki actually help? (seeded-wiki A/B)

Date: 2026-10-01. Backlog X8; ledger claim S3. Branch
`lab/x8-e3-wiki-value` off master `ce0edbe`.
Spend cap: $3.00 metered, hard stop at cap.

## Pre-registration (written and committed before any agent run)

### E3 spec, restated from `evals/tasks/E3-wiki-value.md`

- Claim S3: "Orienting from the wiki improves task outcomes vs a
  no-wiki baseline."
- Pre-registered threshold (spec): "PASS if the wiki arm beats the
  baseline arm on the rubric below across 5 matched tasks, with
  ≤ 25% mean token overhead."
- Design (spec): 5 small realistic tasks (bugfix, extend-a-feature,
  answer-from-history, refactor-per-convention, find-the-decision).
  Arm A: full workspace (AGENTS.md orientation + wiki). Arm B:
  identical repo with `wiki/notes/` emptied and orientation skipped.
  Same model, same tool, interleaved order to wash out drift.
- Rubric per task (spec): correct outcome (0/1); steps/turns to
  completion; input tokens (tool-reported where available; else
  chars/4 estimate, labeled); convention violations (0–n).
- Failure mode the spec names: "A wiki that costs 25% more tokens
  and changes nothing gets its orientation step redesigned or
  dropped. That is a legitimate result."

### Ambiguities in the spec, and the literal choices taken

1. The spec names the 5 task *types* but no concrete tasks, repo,
   or grading tests. Choice: instantiate the 5 types on a seeded
   fixture workspace (`evals/fixtures/x8-e3/workspace/`, a tiny
   billing codebase, "ledgerlite") whose billing rules, money
   convention, refund policy, importer history, and receipts
   decision exist **only** in its wiki notes. This matches the
   backlog's description of E3 as a "seeded-wiki design" distinct
   from S12's real-code design. Using this repo itself was rejected
   for a recorded reason: its wiki facts are duplicated in `docs/`,
   `hidden_files/`, session logs, and code comments (verified by
   grep 2026-10-01, e.g. the telemetry/Postgres decision appears in
   `scripts/sidecar.sh`, `docs/grill-prep.md`, and the wiki note),
   so a no-wiki arm could answer from non-wiki sources — contaminated
   probes, in E2's own terms.
2. "Orientation skipped" in Arm B is not operationalized. Choice:
   Arm B's `AGENTS.md` is the same file with the orientation
   section removed, and `wiki/notes/` is emptied (only `.gitkeep`).
   Everything else — code, README, `wiki/index.md` (titles only, no
   facts), prompts, model, tool — is identical across arms. The
   prompt text is identical across arms; the treatment is files on
   disk only.
3. "Input tokens" is not defined against the Claude envelope's
   cache fields. Choice: token metric = envelope `usage` total
   input = `input_tokens + cache_creation_input_tokens +
   cache_read_input_tokens`, tool-reported. Cost = envelope
   `total_cost_usd` (metered). Turns = envelope `num_turns`.
4. Spec says PASS/FAIL; the ledger needs PROVEN / REFUTED /
   UNVERIFIABLE. Mapping, registered here: **PROVEN** if Arm A
   correct total > Arm B correct total **and** mean total-input-token
   overhead of A over B ≤ 25%. **REFUTED** if A correct total <
   B correct total, **or** A == B with overhead > 25% (the spec's
   own failure mode: costs >25% more and changes nothing).
   **UNVERIFIABLE** otherwise (equal success at ≤25% overhead;
   A > B but overhead > 25%; or a harness failure that prevents
   grading a task pair).

### Tasks (one per spec type; prompts in `evals/fixtures/x8-e3/prompts/`)

| # | Type (spec) | Task | Wiki note(s) carrying the needed facts |
|---|-------------|------|------------------------------------------|
| T1 | bugfix | Fix `invoice_total` in `invoice.py` to the project's billing rules | billing, money-convention |
| T2 | extend-a-feature | Add `refund(amount_cents, *, opened, defective)` per refund policy | refunds |
| T3 | answer-from-history | Write `ANSWER.md`: Feb 2026 import failure + Mar 2026 importer choice | import-history |
| T4 | refactor-per-convention | Refactor `quote` to the money convention | money-convention |
| T5 | find-the-decision | Write `ANSWER.md`: receipts-storage decision + revisit triggers | receipts-decision |

Fixture facts were chosen to be non-default so they cannot be
guessed from convention alone: tax is on the full pre-discount
subtotal and the discount is subtracted after tax; the restocking
fee is 12%; the money convention requires integer cents and half-up
rounding (the legacy code returns float dollars with `round()`);
347 duplicates keyed on row number instead of `external_id`; the
vendor API cap is 100 requests/day with no bulk endpoint; receipts
are append-only JSONL (SQLite rejected, single writer), revisit at
a second concurrent writer, 50,000 lines, or cross-machine queries.

### Grading (from disk only, never agent self-report)

- T1/T2/T4: hidden grading test files (`evals/fixtures/x8-e3/grading/`,
  never copied into a run tree before the run) are overlaid after
  the agent exits and executed by the evaluator. Success = all
  grading tests pass. Convention violations
  = number of failed/error grading tests. Oracle-checked before
  any run: the unmodified fixture fails the grading tests
  (T1 2/5, T2 import error — no `refund`, T4 0/4); a hand-written
  correct implementation passes all of them (T1 5/5, T2 5/5, T4 4/4).
  Pre-run amendment (2026-10-01, before any agent run): the tests
  are plain assert functions executed by a stdlib harness, not
  pytest — pip installs in this sandbox hang and do not persist in
  a scratch venv (observed twice), so grading must not depend on
  pytest. Test content and pass/fail semantics are unchanged.
- T3/T5: `ANSWER.md` on disk is checked against pre-registered
  required token groups and forbidden false-statement strings
  (`grading/answer_checks.json`). Success = file exists, every
  required group present, zero forbidden strings. Convention
  violations = number of forbidden strings found.
- Per run also recorded: turns, metered cost, total input tokens,
  wall seconds, `git diff --stat`.

### Model, tool, order, budget

- Model: the spec names none. Choice, per tasking: the cheapest
  tier used by comparable prior runs — `claude-haiku-4-5-20251001`
  (as in S12), Claude Code 2.1.285 headless, `--output-format json`,
  `--permission-mode acceptEdits`, allowedTools
  `Write Edit Bash Read Glob Grep`, `.claude/settings.json`
  apiKeyHelper (same pattern as `scripts/run_eval.py`). Per-run
  timeout 300 s. Runs execute only in scratch dirs under
  `evals/scratch-x8/runs/` (gitignored).
- Interleaved order (registered): T1-A, T1-B, T2-B, T2-A, T3-A,
  T3-B, T4-B, T4-A, T5-A, T5-B (starting arm alternates per task).
- Budget: $3.00 metered hard cap. Spend is read from each run's
  envelope before launching the next run; if the cap is approached,
  stop launching, grade what exists, and report the achieved n
  honestly (PARTIAL-n).
- Runner: `evals/fixtures/x8-e3/run_x8.py`. Raw outputs: per-run
  result files `evals/results/2026-10-01-RUN-x8-<task>-<arm>.md`
  plus the full JSON envelopes preserved in the scratch run dirs.

## Results

### Incident, run 1 (T1-A, first attempt)

The first T1-A run hit the registered 300 s per-run timeout and was
killed before Claude emitted its JSON envelope: cost and turns are
unmetered for that attempt. Disk grading of its tree: **PASS, 5/5**
(the fix was complete on disk before the kill). A trivial probe
afterwards (`claude -p "Reply with exactly: hi"`, Haiku) took 41 s
of API time for one turn, i.e. API latency, not a hang — 300 s was
below this model's current per-turn latency × expected turns.
Packaged-task runs in this repo use 600–900 s for the same reason.
Amendment (recorded here before any further run): per-run timeout
raised 300 s → 900 s; the timed-out attempt is discarded from the
results table (its PASS is noted, not counted) and T1-A is re-run
once under the amended timeout. Against the $3.00 cap, a
conservative $0.30 reserve is charged for the unmetered attempt
(estimate, labeled — not a metered figure), leaving $2.70 of
metered headroom.

_(results table filled in after the runs)_

### Incident, run 3 (T2-B, first attempt) — cross-run contamination, discarded

T2-B (no-wiki arm) passed its grading 5/5 with an implementation
matching the wiki-only refund policy exactly (12% fee, defective
waiver, half-up). Transcript audit (session
`dedcf36f-1271-4b3e-87b8-fc996f97bdf1`) shows why: the agent ran
`find` over the shared scratch parent and read
`runs/t1-A/wiki/notes/refunds.md` — the Arm A tree left on disk from
the previous run. Same failure family as P2's T1 sandbox escape
(S12 results file). The T1 pair's transcripts were audited and are
clean (own-tree reads only). This T2-B attempt is **discarded**
(its $0.0928468 metered cost is counted in total spend).
Mitigation, applied before any re-run: the runner now keeps only
one live run tree — previous trees are archived with their wiki
notes stripped (notes are identical copies of the committed
fixture, so nothing is lost) — and strips each run's notes after
grading. Every remaining run gets a transcript audit for
out-of-tree reads; a run that reads treatment material is
discarded on the same rule. T2-B is re-run once under the
mitigation; the registered order for the remaining cells is
unchanged (T2-A next after the T2-B re-run, then T3-A, T3-B,
T4-B, T4-A, T5-A, T5-B).

## Verdict

_(per the decision rule registered above)_
