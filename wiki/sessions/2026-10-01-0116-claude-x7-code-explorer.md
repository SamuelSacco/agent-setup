---
session_id: 2026-10-01-0116-claude-x7-code-explorer
tool: claude-code
model: claude-haiku-4-5-20251001 (eval runs)
started: 2026-10-01 01:16 EDT
status: complete
intent: Run X7 kill test for code-explorer exactly per prereg 1228f44 (4 paired exploration tasks, discordant-pair rule, $2.00 cap).
---

# Session: X7 code-explorer kill test

## Intent
Execute evals/results/2026-10-01-X7-code-explorer-prereg.md exactly; disk grading only.

## Starting state
Branch wave2c/x7-code-explorer-kill-test @ 1228f44 (prereg). Scratch ~/workspace/w2c-x7-scratch/ did not exist; runner/grade rebuilt to prereg spec (prompts in runner.py). Snapshot source ~/workspace/p2/w3/scratch/runs/T1-base verified: ground-truth symbols/lines match prereg answer key.

## Turn log

### 01:20 — runs + grading
- **Intended:** execute 8 runs in prereg order, grade from disk.
- **Tried:** runner.py per pair; one batch was SIGTERM'd by the harness after CE3-base, remaining runs executed individually in order; grade.py against the prereg answer key.
- **Happened:** all 8 PASS (base checks 5,4,5,5; agent 5,5,5,5); 0 fabrications after the basename correction recorded in the results file; total metered $0.3496.

### 01:16 — setup
- **Intended:** verify snapshot, build runner.py + grade.py, set repo-local git identity Helm <helm@localhost>.
- **Tried:** grep ground truth on snapshot; wrote runner/grade.
- **Happened:** all CE1/CE2/CE4 symbols match prereg; CE3 function at community.py:499.

## Learned
- Base Haiku passes 4/4 read-only NetworkX tracing tasks (mean 4.75/5 checks) — this task class at this difficulty has no headroom for a specialist discordant win.
- Bare-filename citations (e.g. `flow_matrix.py`) are not fabrications when the file exists in the tree; fabrication grading must resolve basenames, recorded in the results file.

## Outcome
complete — 8/8 runs, $0.3496 of $2.00 cap. Verdict UNVERIFIABLE (S25): 4/4 vs 4/4, zero discordant pairs, agent cheaper ($0.1526 vs $0.1970) so the X7 kill rule is not met and the PROVEN bar is not met. Results: evals/results/2026-10-01-X7-code-explorer-results.md.
