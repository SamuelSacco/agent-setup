---
id: v2-roster
title: Decision — V2 default roster derived from ECC inventory (P2 W2)
type: decision
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [install-surfaces, session-lifecycle]
sources: []
tags: [roster, ecc, canonical]
---

Derived 2026-09-30 (P2 W2, `hidden_files/research/2026-09-30-P2-ecc-mining.md`):
ECC (affaan-m/ECC, MIT) inventoried at 668 items → 19 ported, 223
port-with-changes, 426 skipped. ECC is a catalog, not a setup; the default
roster is selected by job frequency under context rent (ceiling: 7 agents /
8 skills / 4 MCP / 1 hook).

- Default agents: planner, code-reviewer, security-reviewer, tdd-guide,
  build-error-resolver, code-explorer (ECC ports) + V1 backend (kept).
- Default skills: tdd-workflow, verification-loop, search-first,
  codebase-onboarding, documentation-lookup, architecture-decision-records
  (ECC ports) + V1 session-harden, wiki-lint (kept).
- Default MCP: context7, github, sequential-thinking + V1 filesystem-wiki.
  Hook: V1 failure-capture only.
- Demoted to optional: V1 data-scientist (measurement is episodic), V1 ux-ui
  (frontend specialty). Language/stack-specific reviewers, resolvers, and
  pattern skills ship as per-stack optional packs, never defaults.
- Live-tool discovery of the 19 ports is UNVERIFIED (install.sh emits them
  cleanly for both tools; no invocation probe run yet).
