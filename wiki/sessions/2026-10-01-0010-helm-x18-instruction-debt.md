---
session_id: 2026-10-01-0010-helm-x18-instruction-debt
tool: helm
model: Muse Spark
started: 2026-10-01 00:10 EDT
status: complete
intent: Close backlog X18 — verify all 12 prompt-audit suspect patterns and 4 broken references against master ce0edbe, fix any residual, re-run the audit scan to zero.
---

# Session: X18 instruction-debt closure

## Intent
Backlog X18 (docs/experiments-backlog.md) is still marked OPEN, although the
2026-09-30 fix stream (commit 297285e, merged 82ea351) claimed the fixes.
Verify each audit item on disk at ce0edbe; fix what remains; close X18.

## Starting state
- Branch `fix/x18-instruction-debt` off master ce0edbe.
- Audit source: `~/workspace/phase2-prompt-audit-2026-09-30.md` (off-repo;
  summarized in docs/phase2-addendum-2026-09-30.md and wiki/notes/instruction-debt.md).
- Roster on disk: 12 agents, 8 skills, 9 files in scripts/.

## Turn log

### 00:10 — Audit checklist reconstruction + before scan
- **Intended:** Rebuild the 12-pattern / 4-reference checklist from the audit
  report and re-measure at ce0edbe.
- **Tried:** Grep + reference-resolution scan over canonical/, .claude/,
  .github/ (script reproduced in evals/results/2026-10-01-X18-instruction-debt.md).
- **Happened:** Broken references: 0 hits (297285e fixes verified on disk).
  Suspect patterns: 11 of 12 resolved on disk. 1 unresolved: planner.md
  Stripe worked example (audit stale-example #12) — a sizing caveat was
  added in 297285e, but the 77-line maximal-detail example still stands
  at planner.md:103–180 and still anchors full detail as the shown default.

### 00:20 — Residual fix + rescan
- **Intended:** Remove the one unresolved pattern and prove zero.
- **Tried:** planner.md: deleted the 79-line Stripe worked example,
  replaced with a 16-line outline (planner 214 → 151 lines);
  `./scripts/install.sh` regenerated adapters (only the two planner
  mirrors changed; installer `.bak-*` files are gitignored and were
  removed locally). Re-ran the audit scan on this branch and, for the
  before count, on a pristine `ce0edbe` worktree (removed after).
- **Happened:** Before (ce0edbe): broken_references=0,
  suspect_markers=3 (S12 × 3 surfaces), exit 1. After:
  broken_references=0, suspect_markers=0, exit 0. All 80% occurrences
  classified: single labeled definition, labeled references, or
  code-reviewer's confidence threshold (different mechanism).
  Claims-ledger grep for X18 / instruction-debt: 0 hits — no ledger
  change. Evidence written to
  `evals/results/2026-10-01-X18-instruction-debt.md`; backlog X18
  marked CLOSED with resolution note; [[instruction-debt]] gained a
  dated correction.

## Learned
- A backlog item can stay OPEN after its fix merges if the closing edit to
  the backlog is not part of the fix branch — 297285e updated the wiki note
  but not docs/experiments-backlog.md, and missed one audit pattern.
- A sizing caveat on a maximal example does not retire the example as an
  anchor; removal (or a true outline) is the fix the audit's rubric implies.

## Outcome
complete — X18 CLOSED on branch `fix/x18-instruction-debt`. All 12
suspect patterns and 4 broken references dispositioned in the evidence
file; final scan 0 / 0.
