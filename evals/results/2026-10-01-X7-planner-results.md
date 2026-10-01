# X7 Kill Test — planner — Results

Date: 2026-10-01. Pre-registration:
`evals/results/2026-10-01-X7-planner-prereg.md` (commit `7a84210`,
committed before any run). Branch `wave2c/x7-planner-kill-test`.
Protocol: S11 skeleton adapted to planning tasks — 4 paired tasks
on committed fixtures (`evals/fixtures/x7-planner/`), identical
prompts and CLI flags, one variable = `--agent planner`, grading
from disk only against the prereg's fixed answer key.

## Verdict: UNVERIFIABLE

- On the content checks (the part of the key that measures plan
  correctness), all 8 runs score 5/5: 4 concordant pass pairs,
  **zero discordant pairs in either direction** → the PROVEN rule
  (discordant win) is not met.
- Agent arm is cheaper: $0.202 vs base $0.320 (−37%) → the backlog
  X7 kill rule verbatim (no discordant win AND agent cost ≥ base)
  is **not met**. Planner is not killed and does not earn its
  place on this evidence; the test produced no separation.

## Grading artifact — fabrication clause (read before citing)

The prereg's fabrication clause, transplanted verbatim from the
code-explorer tracing protocol, fails any run citing a `.py` path
that does not exist in the fixture. Applied mechanically it gives
base 3/4 vs agent 2/4 (PL2 both arms fail; PL3 agent fails), and
the prereg's fewer-passes clause would then read REFUTED. That
outcome is **not sound evidence**, and it is recorded here rather
than silently used or silently dropped:

- Every flagged path is a file the plan explicitly proposes
  creating, labeled as such in the text: PL2 base —
  `app/password_reset.py` "(new)" (`result.txt:20`),
  `tests/test_password_reset.py` "(new)" (:87); PL2 agent — same
  two, both "(new)" (:20, :25); PL3 agent —
  "`app/posts.py` or new `app/scheduling.py`" (:31).
- For a tracing task, citing a nonexistent path is invention.
  For a planning task, naming a proposed new module is the
  deliverable. The clause measured citation style, not plan
  correctness; the single discordant pair it produces (PL3)
  turns on one parenthetical "(or new …)".
- The verdict above therefore follows the governing backlog kill
  rule on the sound part of the evidence (content checks +
  cost). A decisive rerun needs one prereg fix: scope the
  fabrication clause to paths cited as existing code.

## Per-pair outcomes

Checks = content checks hit (x/5). Fab = fabrication flags under
the literal clause (all proposed-new files, see above).
Cost/turns from the JSON envelopes, ledger-verified 8/8.

| Task | Base checks | Agent checks | Pair | Base $ / turns | Agent $ / turns |
|------|------|------|------|------|------|
| PL1 low-stock alert | 5/5 | 5/5 | concordant | 0.0413 / 10 | 0.0463 / 16 |
| PL2 password reset | 5/5 (fab: 4 proposed) | 5/5 (fab: 3 proposed) | concordant | 0.1307 / 16 | 0.0477 / 15 |
| PL3 scheduled publishing | 5/5 | 5/5 (fab: 1 proposed) | concordant on content; discordant loss under literal fab clause | 0.0766 / 14 | 0.0482 / 14 |
| PL4 failed-charge retry | 5/5 | 5/5 | concordant | 0.0712 / 14 | 0.0598 / 13 |

Totals: base $0.31983 (54 turns), agent $0.20204 (58 turns).
Mean checks: 5.0 per task, both arms. No fabrication of existing
code in any run (every cited existing path verified on disk by
the grader's basename/exact-path check — the flags are only the
proposed-new paths listed above).

## Spend

Metered total (Claude JSON envelopes): **$0.52187 of the $2.00
hard cap**. No run approached the $0.60 single-run soft cap
(max $0.1307). Caveat: one PL2-base attempt was killed mid-run by
a host SIGTERM before writing its envelope; its spend is
unmetered and unknown, and the pair was re-run fresh (the re-run
is the graded PL2 base above). All other runs rc=0.

## Notes

- Fixture traps were found by both arms on every task (hash-only
  token storage, worker-only retries with the original
  idempotency key, `now_utc` convention, crossing-only alerts):
  at this fixture size (~70–90 lines), Haiku base has no headroom
  left for a planner win — same ceiling pattern as S22/X10.
  A decisive test needs harder/larger codebases, plus the
  fabrication-clause fix above.
- Artifacts: runner, prompts, envelopes, grades in
  `~/workspace/w2c-x7-planner-scratch/` (`runner.py`, `grade.py`,
  `runs/`, `ledger.tsv`, `grades.json`).
