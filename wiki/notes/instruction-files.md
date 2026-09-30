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
- Robust bridge (used here): `CLAUDE.md` first line `@AGENTS.md`, Claude-only 
  notes below. Never double-loads; verify with `/context`.
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
  2/2 both canaries). Decision: keep the `@AGENTS.md` bridge — dropping
  CLAUDE.md also loses the annex and `InstructionsLoaded` hook firing.
