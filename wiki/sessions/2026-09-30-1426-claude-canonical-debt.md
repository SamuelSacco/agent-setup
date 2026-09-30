---
session_id: 2026-09-30-1426-claude-canonical-debt
tool: claude-code
model: Muse Spark (subagent)
started: 2026-09-30 14:26 EDT
status: complete
intent: Fix canonical/ instruction debt and broken references per the 2026-09-30 prompt audit; branch fix/canonical-debt off phase-2.
---

# Session: Canonical instruction-debt fixes (W1)

## Intent
Samuel's 14:24 ET directive: comprehensive review, repo into a good state, merge to master. This stream owns the canonical/ fixes sourced from `phase2-prompt-audit-2026-09-30.md`: 4 broken references, the unsourced 80% coverage constant (11 locations), emphasis boosters, verification/checkpoint rituals, and one stale Playwright example.

## Starting state
- Fresh clone at ~/workspace/p3/fixes, branch phase-2 @ head, new branch fix/canonical-debt.
- Canonical roster verified on disk: 12 agents, 8 skills. No `researcher` agent, no `architect` agent (canonical: `code-architect`), no `security-review` skill, no `scripts/setup-package-manager.js`.
- CLAUDE.md out of scope (separate stream).

## Turn log

### 14:26 — Orientation + session start
- **Intended:** Orient per root AGENTS.md; confirm roster from disk before rewiring references.
- **Tried:** Read wiki/index.md, wiki/log.md tail, AGENTS.md; `ls canonical/agents canonical/skills scripts`.
- **Happened:** Roster matches audit scope. Session record created.

### 14:35 — Broken references rewired
- **Intended:** Every named agent/skill/script in canonical/ resolves to a real file.
- **Tried:** search-first.md: `researcher` (5 sites) → subagent delegation / research pass; `architect` → `code-architect`; `iterative-retrieval` section → progressive-discovery cycles within the skill. security-reviewer.md:104 `security-review` → `verification-loop`. build-error-resolver.md:107 `architect` → `code-architect`. tdd-workflow Step 0: `scripts/setup-package-manager.js --detect` mandate → detect from `packageManager` field / lockfile / env. tdd-workflow Bun section: `bun-runtime` skill pointer removed. doc-updater.md (found by the checker, not the audit): `scripts/codemaps/generate.ts` command → codemaps are workflow-generated; `/update-codemaps`/`/update-docs` backing claim removed from description.
- **Happened:** All rewires applied. One process failure logged honestly: the search-first diagram-line replacement was issued in the same parallel block as other edits and did not persist; caught by the verification sweep and re-applied sequentially.

### 14:42 — Instruction debt trimmed
- **Intended:** Remove the audit's SUSPECT patterns without touching load-bearing procedure.
- **Tried:** 80% coverage: defined ONCE in tdd-workflow Core Principle 2 as a labeled heuristic default (project config overrides); 10 repetitions across tdd-workflow/tdd-guide/planner/verification-loop converted to references. code-reviewer description: "MUST BE USED for all code changes" → trigger (after a change, before commit/handoff). verification-loop: 15-minute re-verification → event-driven rule; `/verify` pseudo-command removed. tdd-workflow: Git Checkpoints principle cut from 10 policing rules to 4 mechanism lines; Steps 3/5/6 checkpoint blocks → pointers; Step 8 evidence-report document → report = quoted test output. tdd-guide: pass@1/pass@3 addendum → release-critical paths only, run counts recorded. Playwright example: `waitForTimeout(600)` → auto-retrying count assertion; `2025-12-31` fill → computed date +30d. Closing "Remember" boosters deleted in security-reviewer and tdd-workflow; security-reviewer closing booster at :108 also removed.
- **Happened:** All applied. code-reviewer ">80% confident" left untouched — reporting-confidence threshold, a different mechanism from the coverage constant.

### 14:48 — Verification + adapter regeneration
- **Intended:** Prove the fixes; keep adapter output consistent with canonical/.
- **Tried:** Scripted reference-resolution pass (extract agent/skill/script names from reference patterns in canonical/*.md; check against on-disk roster) run against phase-2 baseline and this branch. Then `./scripts/install.sh` per AGENTS.md §4.
- **Happened:** Baseline: 4 unresolved references, 11 known-broken identifier hits. After: 0 failures, all identifiers absent, every remaining 80% is the definition or a labeled reference. install.sh changed exactly the 18 adapter mirrors of the 9 edited canonical files; spot-checked clean.

## Learned
- The audit undercounted broken references: the checker found two more (`bun-runtime` was in the audit; `scripts/codemaps/generate.ts` and the `/update-*` command claim in doc-updater were not).
- Parallel edit blocks can silently drop a write; verification sweeps must run after, sequentially.

## Outcome
complete — branch fix/canonical-debt ready to push. No claims-ledger change (no entry asserted the fixed content; invocable file names unchanged). CLAUDE.md untouched (separate stream). Durable facts hardened into [[instruction-debt]].
