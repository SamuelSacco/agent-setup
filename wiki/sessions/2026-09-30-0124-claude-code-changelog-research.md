---
session_id: 2026-09-30-0124-claude-code-changelog-research
tool: claude-code
model: unknown (subagent)
started: 2026-09-30 01:24 EDT
status: complete
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

### 01:35 — Claude Code changelog lane landed
- **Intended:** Get dated, version-pinned Claude Code audit (v2.1.105 → v2.1.285) from official changelog.
- **Tried:** Child agent audited raw CHANGELOG.md + dated changelog + v2.1.285 release page + advisor docs. Deliverable: `/tmp/changelog-claude-code.md`.
- **Happened:** Complete. High-value: `OTEL_LOG_RAW_API_BODIES` added v2.1.111 (Apr 16), `file:` mode improved v2.1.274 (Sep 17); `PostToolUseFailure` existed by v2.1.119 (Apr 23) but its introduction is NOT in the changelog (no entry); AGENTS.md fallback v2.1.277 (Sep 18), provider restriction lifted v2.1.281 (Sep 23); no `.agents/skills` discovery; advisor is session-level, Anthropic-API-only; Sonnet 5.5 default v2.1.284 (Sep 28), Opus 5.5 default v2.1.280 (Sep 22). Four ⚠ CHECK flags (C2/C3/C4/S4) recorded for synthesis — none overturn a ledger verdict; C4's provider caveat is now historical. Awaiting Copilot lane (still running) before writing final file.

### 01:40 — Copilot lane landed; synthesis written; hardened
- **Intended:** Merge both lanes into `hidden_files/research/2026-09-30-changelogs.md` with ledger flags; harden session per house rules.
- **Tried:** Read `/tmp/changelog-copilot-cli.md`; wrote combined file (Part 1 Claude Code, Part 2 Copilot CLI, Part 3 ledger cross-checks + summary). Checked `wiki/notes/instruction-files.md` for the C4 provider caveat (absent there — caveat lives only in the research brief, so no note edit); appended `wiki/log.md`.
- **Happened:** Deliverable complete. Copilot lane's decisive find: `postToolUseFailure` exists since v1.0.15 (2026-04-01) and repo hooks load since v1.0.49 — but prompt mode gates repo hooks behind trust / `GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS` (v1.0.40), which predicts E4's 0/5 headless without any missing loader. S4's Copilot mechanism attribution is flagged for a trusted-mode re-test; verdicts unchanged.

## Learned
- Claude Code: `OTEL_LOG_RAW_API_BODIES` v2.1.111 (2026-04-16); `file:<dir>` linking improved v2.1.274 (2026-09-17). No `PostToolUseFailure` introduction entry exists — existence proven only by v2.1.119.
- Claude Code: AGENTS.md fallback v2.1.277 (2026-09-18); provider restriction lifted v2.1.281. No `.agents/skills` discovery. Advisor = session-level, Anthropic-API-only, needs feature-flag fetching (off when telemetry/flags disabled). Sonnet 5.5 default v2.1.284; Opus 5.5 default v2.1.280; effort is per-model since v2.1.251.
- Copilot CLI: hooks ship (`postToolUseFailure` v1.0.15; `.github/hooks/` v1.0.49; 15 events; dual camelCase/PascalCase dialects) but prompt mode trust-gates repo hooks (v1.0.40). `/env` (v1.0.60) is the verification surface. OTel file exporter + content capture is the dependable cross-harness plane. BYOK has two config generations (`providers.json` > legacy env vars). Copilot consumes `.agents/skills`, `.claude/skills`, `.claude/agents`, `.claude/rules`; Claude consumes none of `.agents/*`.
- Hardened into: `hidden_files/research/2026-09-30-changelogs.md` (full audit + flags); no durable-note edit required (C4 caveat was brief-only).

## Outcome
complete — deliverable written; no ledger verdict overturned; one re-test owed (S4 Copilot leg, trusted mode) before the deck cites the hook refutation.
