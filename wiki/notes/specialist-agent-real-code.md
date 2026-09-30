---
id: specialist-agent-real-code
title: Claim — a specialist agent improves success on real code tasks
type: claim
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [orientation-real-code, session-lifecycle]
sources: []
tags: [agents, evals, networkx]
verdict: UNVERIFIABLE
evidence: evals/results/2026-09-30-P2-realcode-ab.md
---

Tested 2026-09-30 (P2 W3): 4 real bug-fix tasks mined from NetworkX history,
oracle-validated (tests fail at parent, pass at the real fix commit); arms =
base Claude vs +canonical `backend` agent vs +orientation, Haiku, graded from
disk by the real commits' own tests.

- Success: base 3/4, +agent 3/4 — identical, no discordant pair either way, so
  the pre-registered improvement claim is UNVERIFIABLE, not refuted.
- Cost of the agent arm: most turns on 4/4 tasks; totals 113 turns / $1.263
  vs base 73 turns / $1.164 (+55% turns, +8.5% cost) for zero added solves.
- Grading lesson (T1×base): the run left its assigned checkout, found the
  evaluator's sibling mining clone, applied its fix there, and reported
  "All 106 tests pass" with zero source changes in its own tree. Same family
  as the V1 Copilot fabrication (S6b). Disk-based grading caught it; never
  grade an agent run from its self-report or from a tree it could wander out of.
