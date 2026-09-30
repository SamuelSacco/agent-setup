---
id: orientation-real-code
title: Claim — orientation (AGENTS.md/wiki context) improves success on real code tasks
type: claim
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [specialist-agent-real-code, instruction-files]
sources: []
tags: [orientation, evals, networkx]
verdict: PROVEN
evidence: evals/results/2026-09-30-P2-realcode-ab.md
---

Tested 2026-09-30 (P2 W3, same design as [[specialist-agent-real-code]]):
the +orientation arm solved 4/4 NetworkX tasks vs base 3/4 — the discordant
win was T1 (ISMAGS), the hardest task — and it was the cheapest Claude arm
overall (77 turns, $0.967 vs base 73 turns, $1.164).

Verdict PROVEN at the pre-registered bar, with the stated caveat: the margin
is one discordant pair at n=4. Direction is consistent (only arm to solve T1;
lowest total cost) but a larger n is required before generalizing beyond
this repo/task mix.
