---
session_id: 2026-09-30-0124-claude-code-changelog-research
tool: claude-code
model: unknown (subagent)
started: 2026-09-30 01:24 EDT
status: in-progress
intent: Audit official Claude Code + Copilot CLI changelogs (last ~3–6 months) for telemetry/hooks/instructions/skills/agents/MCP changes; flag contradictions with claims ledger.
---

# Session: Changelog audit for both CLIs

## Intent
Parent task: bring us current on both CLIs from official changelogs only. Web research; no CLI runs; no API spend. Output: `hidden_files/research/2026-09-30-changelogs.md`, terse engineering prose, with anything that contradicts or postdates `docs/claims-ledger.md` flagged.

## Starting state
Claims ledger read (C1–C4, S1–S7; ledger dated 2026-09-30). House rules read (AGENTS.md). Wiki oriented (index, data-model, log tail). Installed versions per parent: Claude Code v2.1.285, Copilot CLI v1.0.89.

## Turn log

### 01:24 — Orient + session open
- **Intended:** Follow house rules before research.
- **Tried:** Read AGENTS.md, claims-ledger.md, wiki/index.md, wiki/data-model.md, wiki/log.md tail, session template.
- **Happened:** Oriented. Delegating the two changelog lanes to parallel child agents; synthesizing here.

### 01:26 — Changelog lanes delegated; ledger cross-refs loaded
- **Intended:** Parallelize Claude Code vs Copilot CLI changelog audits; prep contradiction flags against ledger C1–C4/S4.
- **Tried:** Spawned two web-research children (official sources only; no CLI runs; no API spend). Read sibling `hidden_files/research/2026-09-30-copilot-cli-docs.md` (docs-axis verdicts) and grepped prior research for version gates (AGENTS.md v2.1.277/2026-09-18; /import v2.1.213+; /doctor prompt-audit v2.1.283+).
- **Happened:** Children running. Copilot docs-axis already PROVEN (OTel file exporter, hooks documented with no version gate) — changelog lane must supply the *version/date* history docs pages omit; key open flag: whether hooks shipped in a Copilot CLI version after v1.0.89, which would qualify S4's REFUTED.
