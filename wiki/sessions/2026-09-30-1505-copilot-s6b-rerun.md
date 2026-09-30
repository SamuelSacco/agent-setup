session_id: 2026-09-30-1505-copilot-s6b-rerun
tool: copilot-cli
model: claude-haiku-4-5-20251001 (BYOK, Anthropic)
started: 2026-09-30 15:05 EDT
status: complete
intent: Re-run the E6 Copilot leg (backend agent, TokenBucket task) with writes pre-approved and disk-grade it, to close the S6b fairness gap.
---

# Session: S6b pre-approved Copilot rerun

## Intent
Ledger S6b is REFUTED (pilot) but audit-scoped: the pilot ran under default
permissions (writes denied from the first file) while Claude's S6a pass ran
pre-approved. Re-run the identical bounded task on Copilot with writes
pre-approved (`COPILOT_ALLOW_ALL=true` + `--allow-all-tools`), disk-grade
the result, and amend S6b with the outcome. Samuel's 2026-09-30
repo-hardening program; unattended allow-all authorized for eval scratch.

## Starting state
- Branch `exp/s6b-preapproved` off origin/phase-2 @ 17b3054, clone
  `~/workspace/p3/s6b-rerun`.
- Pilot (2026-09-30 ~01:40 ET): `--agent backend`, BYOK Haiku, exit 0,
  `Changes +0 -0`, no files written, fabricated "22 passed in 1.23s".
- S6a (Claude rerun, pre-approved): ratelimit.py + test_ratelimit.py on
  disk, independent pytest re-run 13 passed, $0.0767 metered, 11 turns.
- Copilot CLI 1.0.89 at ~/workspace/tools/bin/copilot.

## Turn log
<!-- Append one entry per meaningful step. Never edit past entries. -->

### 15:05 — Orientation + setup
- **Intended:** replicate pilot fixture and grading exactly.
- **Tried:** read E6 task, E6 pilot, E6 Claude rerun, byok-probe,
  pv-copilot.sh, run_eval.py copilot arm; created fresh fixture copy with
  install.sh run; pre-run md5 snapshot; grading venv with pytest.
- **Happened:** fixture ready (261-file snapshot, backend.agent.md
  emitted, task files absent), grading venv with pytest 9.1.1.

### 15:07 — Copilot run, writes pre-approved
- **Intended:** one run, `COPILOT_ALLOW_ALL=true` + `--allow-all-tools
  --allow-all-paths`, `--agent backend`, BYOK Haiku (same as pilot).
- **Tried:** single `copilot -p` invocation from the fixture root,
  prompt = pilot/S6a bounded task (verbatim in the results file).
- **Happened:** exit 0, wall 98 s, `Changes +245 -3`, tokens ↑ 367.3k
  (327.4k cached) • ↓ 5.2k. Zero "Permission denied" lines. Agent's own
  loop: 18/20 → fixed two wrong test assertions → 20/20.

### 15:10 — Disk grading
- **Intended:** grade from disk only.
- **Tried:** md5 diff vs snapshot; independent pytest re-run in a fresh
  venv; grader-written contract probe (burst / empty-deny / refill).
- **Happened:** `ratelimit.py` 1,736 B + `test_ratelimit.py` 6,092 B
  (20 tests) on disk; grader re-run **20 passed, exit 0**; contract
  probe passed. Self-report matched disk this time.

## Learned
- S6b's pilot REFUTED was a permission-mode artifact, not a capability
  result: with writes pre-approved, Copilot's `backend` agent completes
  the same bounded task Claude's did (S6a), with comparable artifacts.
  Any cross-tool comparison that mixes permission modes is invalid.
- Copilot self-report is checkable either way: in the pilot it
  fabricated "22 passed" over zero files; in this rerun its "20/20"
  was accurate. Disk grading is what distinguishes the two.

## Outcome
complete — verdict PROVEN (n=1, scoped) for "Copilot backend agent
completes the bounded task when writes are pre-approved"; S6b amended
(pilot record kept); S6 parity grid still UNVERIFIABLE. Spend $0.39
converted of $2 cap. Results:
evals/results/2026-09-30-S6B-preapproved-rerun.md (+ transcript).
