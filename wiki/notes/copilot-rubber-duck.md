---
id: copilot-rubber-duck
title: Claim — Copilot CLI ships a "rubber duck" critic agent
type: claim
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [claude-advisor]
sources: []
tags: [copilot, review]
verdict: PROVEN
evidence: hidden_files/research/claims-tips.md
---

PROVEN. Built-in, read-only critic agent that runs on a **different model 
family** than the session driver (Claude↔GPT) to avoid shared blind spots. 
Auto-consulted at high-leverage moments; manual via "rubber duck your plan", 
`/rubber-duck`, or `copilot --agent rubber-duck`.

Interesting symmetry with [[claude-advisor]]: both tools now pair a driver with 
a second model's judgment — Anthropic uses a *stronger same-vendor* advisor, 
GitHub uses a *cross-vendor* critic. Worth one slide.
