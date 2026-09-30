---
id: instruction-files
title: Instruction files — AGENTS.md is the shared layer (with traps)
type: reference
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [session-lifecycle]
sources: []
tags: [instructions, claude, copilot]
---

Researched 2026-09-30 from Anthropic + GitHub docs (full brief: 
`hidden_files/research/instructions-files.md`).

- `AGENTS.md` is the shared instruction layer: Codex, Copilot (CLI/IDE/cloud), 
  Cursor, Gemini CLI, Devin and others read it natively. Stewarded by the 
  Agentic AI Foundation (Linux Foundation) since 2025-12-09.
- **Claude Code joined 2026-09-18 (v2.1.277)** — but conditionally: it reads 
  `AGENTS.md` only when NO `CLAUDE.md`/`CLAUDE.local.md` exists in cwd or above. 
  "Claude Code doesn't read AGENTS.md" is now REFUTED (outdated).
- Robust bridge: `CLAUDE.md` first line `@AGENTS.md`, Claude-only
  notes below. Never double-loads; verify with `/context`.
  **Superseded in this workspace 2026-09-30 (W3):** CLAUDE.md deleted;
  the shared file loads natively and `scripts/check-agents-md-load.sh`
  guards the invariants (see below). The bridge remains the fallback
  for trees that cannot guarantee the version floor.
- Copilot CLI **combines** all applicable instruction files with no defined 
  precedence (github.com surfaces have one; the CLI is not github.com).
- Unification is instruction-text only: permissions, hooks, sandboxing remain 
  per-tool — which is exactly what the adapter layer is for.
- **P2 W5 canary probes** (2026-09-30, `evals/results/2026-09-30-P2-claudemd-drop.md`):
  native AGENTS.md load PROVEN when no CLAUDE.md exists in cwd/ancestors
  (2/2, loader debug line captured). Trap PROVEN (2/2): an annex-only
  CLAUDE.md (no `@AGENTS.md` import) silently suppresses the shared file —
  zero transcript hits. Both-files mode is settable headlessly via user
  settings `pluginConfigs` (`instructionFiles: "claude-md-and-agents-md"`,
  2/2 both canaries). Decision at the time: keep the `@AGENTS.md` bridge —
  dropping CLAUDE.md also loses the annex and `InstructionsLoaded` hook firing.
- **W3 final-shape proof** (2026-09-30, `evals/results/2026-09-30-P2-claudemd-final-shape.md`):
  under Samuel's directive the decision was reversed WITH a guard.
  CLAUDE.md deleted on branch `change/no-claudemd`; final shape re-proven
  live (Claude 2.1.285 marker load 2/2 with loader debug line, Copilot
  1.0.89 1/1). `scripts/check-agents-md-load.sh` fails on: Claude
  < 2.1.277 with no CLAUDE.md; any CLAUDE.md lacking the `@AGENTS.md`
  bridge; a failed live marker probe. Negative controls exit 1 (static,
  and live probe answered NOT LOADED). Guard runs as run-eval's
  preflight. Accepted losses: the annex (its `/context` tip now refers
  to AGENTS.md) and `InstructionsLoaded` firing for the main file.
  Ledger claim C4 amended.

## Copilot custom agents DO receive AGENTS.md (X17, behavioral)

The v1.0.86 changelog says repo instruction files are opt-in per
custom agent (`include-custom-instructions: true`), and our emitted
agents don't set it. Probed behaviorally 2026-09-30 (CLI 1.0.89,
`--agent backend`, body-only marker in a scratch AGENTS.md): the
as-emitted agent reproduced the marker exactly with zero tool calls;
flag-on was identical; marker-removed control failed. Debug log shows
AGENTS.md injected as a `<custom_instruction>` block alongside
`<agent_instructions>`. **PROVEN for the CLI `--agent` surface
(ledger S18)** — the changelog statement may describe other surfaces
(IDE/cloud), which remain untested. Evidence:
`evals/results/2026-09-30-X17-copilot-agent-orientation.md`.
