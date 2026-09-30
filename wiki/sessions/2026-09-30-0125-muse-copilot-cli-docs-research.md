---
session_id: 2026-09-30-0125-muse-copilot-cli-docs-research
tool: claude-code
model: Muse subagent (docs research)
started: 2026-09-30 01:22 EDT
status: complete
intent: Verify or refute Copilot CLI telemetry/prompt-lifecycle claims against official GitHub docs only.
---

# Session: Copilot CLI docs verification

## Intent
Check eight claim groups (OTel support, file-exporter auto-enable, content
capture fields, wire-body distinction, logging flags, hooks, instruction
files, BYOK env vars) against docs.github.com and record verdicts with
deciding quotes.

## Starting state
- Docs research only; no CLI runs, no API tokens spent.
- Prior local result on record: Copilot CLI v1.0.89 did not execute repo
  hooks (E4, 0/5) despite documented format.

## Turn log

### 01:22 — parallel docs research
- **Intended:** verify claims from official docs with exact quotes.
- **Tried:** three parallel research streams (OTel/telemetry, hooks,
  instruction files + BYOK) over docs.github.com.
- **Happened:** all claims resolved. Findings written to
  `hidden_files/research/2026-09-30-copilot-cli-docs.md`.

## Learned
- Copilot CLI OTel claims all PROVEN in docs, including file-exporter
  auto-enable and full `gen_ai.*` content capture; capture is a
  semantic-convention span representation, not a raw HTTP wire body.
- Hooks documented as shipped (`.github/hooks/*.json`, schema `version: 1`,
  14 events incl. `postToolUseFailure`); no preview marker, no minimum CLI
  version stated. The v1.0.89 no-execution result stays unexplained by docs.
- Instruction files merge with no documented precedence; `COPILOT.md`
  REFUTED as a documented CLI instruction file.
- BYOK: all four `COPILOT_PROVIDER_*` vars documented; `COPILOT_MODEL`
  also required; `providers.json` registry overrides env vars.

## Outcome
complete — verdicts delivered in the research file for the parent agent to
fold into `docs/claims-ledger.md` as needed.
