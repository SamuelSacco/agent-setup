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

## Correction — 2026-09-30 (W2 triage lab)

This note records the earlier W2 derivation and is no longer the roster
of record. The packet (`docs/phase2-packet-2026-09-30.md`) carries a
different roster v2 (default: explorer, code-reviewer, task-runner,
build-error-resolver, security-reviewer, evaluator; provisional: planner,
code-explorer) — which itself exists only on paper: `canonical/agents/`
has no `task-runner` or `evaluator` file, and "explorer" vs provisional
"code-explorer" appear to name the same file. The line above claiming
live-tool discovery is UNVERIFIED is overtaken: ledger S14 (PROVEN,
2026-09-30) live-invoked all 12 agents and 8 skills in both tools.
Three sources currently tell three roster stories; reconciling them is
backlog X20 in `docs/experiments-backlog.md`. Do not cite this note for
the current roster.
