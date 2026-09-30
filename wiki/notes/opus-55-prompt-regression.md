---
id: opus-55-prompt-regression
title: Claim — Opus 5.5 makes older prompts behave worse
type: claim
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [session-lifecycle]
sources: []
tags: [claude, models]
verdict: UNVERIFIABLE
evidence: hidden_files/research/opus-55-prompt-claim.md
---

As a general claim: **UNVERIFIABLE** — no primary source or controlled study 
supports it; the most-cited explainer post contains factual errors (XML is not 
deprecated; tool format unchanged; 1M context is standard).

Narrowly supported patterns: prefilled final-turn responses now return 400; 
leaving `effort` unset changes token budgets; prompts forcing exhaustive 
visible step-by-step reasoning may show less surface reasoning because more 
happens internally. That is retuning advice, not a regression.

Presentation line: "Retune prompts that depended on forced visible reasoning — 
that's optimisation, not a regression."
