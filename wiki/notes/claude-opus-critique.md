---
id: claude-opus-critique
title: Pre-merge red-team critique by Claude Code (Opus 5.5) — 2 BLOCKERs, ledger corrections
type: claim
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [orientation-real-code, ecc-ports-invocable]
sources: []
tags: [review, merge-gate]
verdict: PARTIAL
evidence: docs/claude-critique-2026-09-30.md
---

Full critique: `docs/claude-critique-2026-09-30.md` (Claude Code 2.1.285, model claude-opus-5-5, orchestrated + spot-verified by Helm; 8 of 8 headline spot-checks CONFIRMED, 1 reviewer sub-claim WRONG and corrected in-doc).

Headline outcomes:
- **S12 BLOCKER**: PROVEN survives only narrowed — the tested treatment was a hand-written orientation file (CLAUDE.md), not this repo's AGENTS.md/wiki. S3 (wiki) stays UNVERIFIABLE. Combined rule was registered after the NetworkX result.
- **S4 BLOCKER**: ledger carried a Copilot mechanism ("no hook loader") that E4.md's addendum retracts; leg corrected to PARTIAL-with-mechanism.
- **S14 downgraded PROVEN → PARTIAL** (playwright REFUTED as-shipped in both tools in the tested environment).
- **S5 corrected**: corpus-truth score 5/10 (not 6/10); "−51% inputs" is uncached-only, total input −2%.
- **S6b scoped**: REFUTED only under default permissions; capability reading UNVERIFIABLE (pilot was permission-blocked, never rerun under trust).
- Narrative: packet cites 4 research files not on the branch; `quickstart.sh` claimed at packet:83-85 but not shipped. 2 narrative fixes applied (packet:21 quote, addendum:33 token range).
- Setup soundness (17 findings): worst — `scripts/adapters.py` drops `tools_hint`, so read-only agents (planner, code-explorer) run with full tool access in both tools; failure-capture payloads land in git-tracked `wiki/telemetry/events.jsonl`.
- CLAUDE.md verdict: keep the bridge until every user is guaranteed Claude Code ≥2.1.281 with the agents-md plugin; then delete and move the annex to `.claude/rules/`.
