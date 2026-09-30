---
id: instruction-debt
title: Canonical instruction debt — fixed 2026-09-30 (branch fix/canonical-debt)
type: procedure
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [opus-55-prompt-regression, session-lifecycle]
sources: []
tags: [canonical, prompts, tdd]
---

# Instruction debt in canonical/

Findings from the 2026-09-30 prompt audit (12 SUSPECT patterns, 0 contradictions;
debt concentrated in the two ECC-derived TDD files). Fixed on `fix/canonical-debt`:

- **Broken references (all rewired or removed; verified 0 unresolved):**
  `researcher` agent (search-first, 5 sites) → subagent delegation / research pass;
  `architect` → `code-architect` (search-first, build-error-resolver);
  `security-review` skill (security-reviewer) → `verification-loop`;
  `scripts/setup-package-manager.js` mandate (tdd-workflow Step 0) → detect from
  `packageManager` field / lockfile; `bun-runtime` skill pointer and
  `iterative-retrieval` skill section removed (neither exists);
  `scripts/codemaps/generate.ts` (doc-updater) → workflow-generated, no script.
- **80% coverage constant:** defined ONCE as a labeled heuristic default in
  `tdd-workflow` Core Principle 2 ("not a measured optimum and not a law";
  project config overrides). All other occurrences are references to it.
  code-reviewer's ">80% confident" is a different mechanism (reporting
  confidence) — not the coverage constant, left as-is.
- **Rituals trimmed to mechanism:** git checkpoints at phase boundaries only
  (RED/GREEN); Step 8 evidence-report document → report = quoted test output;
  verification-loop re-verification is event-driven (on change / before PR /
  before claiming done), never calendar-driven; pass@1/pass@3 addendum →
  release-critical paths only, record run counts not rate labels.
- **Boosters removed:** code-reviewer "MUST BE USED for all code changes" →
  trigger = after a change, before commit/handoff; security-reviewer and
  tdd-workflow closing "Remember" paragraphs deleted.
- **Stale example:** Playwright E2E example — `waitForTimeout(600)` replaced
  with an auto-retrying `expect(...).toHaveCount(...)`; hard-coded
  `2025-12-31` fill replaced with a computed date 30 days out.

Verification method: scripted reference-resolution pass over canonical/*.md —
extract agent/skill/script names from reference patterns, check against the
on-disk roster (12 agents, 8 skills, 6 scripts, 5 MCP). Before: 4 unresolved
references + 11 known-broken identifier hits. After: 0 failures, all absent.
Adapter output (.claude/, .github/) regenerated via `scripts/install.sh`.

No claims-ledger change: no ledger entry asserted the fixed content; file
names (the invocable surface behind S14/S15) are unchanged.
