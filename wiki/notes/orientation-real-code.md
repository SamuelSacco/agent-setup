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

Replication (2026-09-30, P2 port-verification session, same results file):
4 new tasks mined and oracle-validated the same way; orientation again
4/4 vs base 3/4 with the discordant win on R2 and no discordant loss.
Combined n=8: base 6/8, orientation 8/8, both discordant pairs favor
orientation, combined cost at parity (base $1.826 / orientation $1.865).
One honesty note on R2: base raised the right exception type with the
message "No nodes in graph" and failed the real test's `null graph`
message match — the pair turns on message wording, not behavior class.

Copilot arm (2026-09-30, evals/results/2026-09-30-P2-copilot-ab.md):
same 8 tasks, Copilot CLI BYOK Haiku — UNVERIFIABLE. Only 2 of 8 pairs
completed before the $4 budget gate stopped the rest (Copilot converts
at 3–9× Claude's cost per task; 1.7–2.0M input tokens on T1/R2). Both
completed pairs are concordant passes (base 2/2, +orientation 2/2, no
discordant pair). Copilot base is 3/3 across every task it has run in
this project (T1, T3, R2 — including R2, a Claude discordant pair), so
the completed pairs had no headroom for an orientation win. On both
completed pairs +orientation cost and wall time ran *above* base —
opposite direction from the Claude arms, n=2, no cost threshold
pre-registered.

Second codebase (2026-09-30, same results file, pre-registered
extension): the identical experiment on Textualize/rich — 4
oracle-validated tasks (pretty, console, cells, table), base vs
+orientation, same model. Result: 3/4 vs 3/4, zero discordant pairs;
U3 (cell widths for ZWJ sequences) was failed identically by both
arms with the same partial fix. Claim B on Rich alone:
UNVERIFIABLE. Combined n=12: base 9/12, orientation 11/12 — PROVEN
stands under the pre-registered combined rule, with both discordant
pairs still NetworkX's. The second codebase is consistent with the
claim but adds no independent confirmation; the higher Rich base
solve rate (3/4) left little headroom.

Model-tier test (2026-09-30, P3 E1, ledger S18,
evals/results/2026-09-30-P3-bigmodel-ab.md): the identical protocol
on claude-opus-5-5 — NetworkX 3/4 vs 3/4, Rich 3/4 vs 3/4, zero
discordant pairs anywhere. Verdict at that tier: UNVERIFIABLE. The
mechanism is base movement, not orientation harm: Opus base solves
T1 (the Haiku discordant pair), and the tasks that still fail (T4,
U3) fail identically in both arms at both tiers. Read S12 as a
Haiku-tier result: orientation paid when the base model left
headroom on a hard task; at the top tier, on this task mix, there
was no headroom left for it to buy — while still charging ~+9%
context rent per run.
