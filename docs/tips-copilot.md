# Tips & Tricks — GitHub Copilot CLI

Researched 2026-09-30 against GitHub's docs. Verdicts in `docs/claims-ledger.md`.

## Rubber duck — the built-in cross-model critic **[PROVEN]**

- Copilot CLI ships a **rubber duck agent**: an independent critic that reviews 
  plans, code, and tests with severity-categorized feedback (Blocking / 
  Non-blocking / Suggestions).
- The trick: it deliberately runs on a **different model family** than your 
  session (Claude driving → GPT critic, or vice versa) so it doesn't share the 
  driver's blind spots.
- Auto-consulted after planning non-trivial changes, mid-implementation, after 
  tests, and after repeated failures. Skipped for small changes.
- Invoke manually: "Rubber duck your plan", `/rubber-duck <prompt>`, or start as 
  one: `copilot --agent rubber-duck`.
- Read-only: explores but never edits. Costs extra model usage per consult — 
  GitHub's bet is early catches pay for it. Test that bet (evals/) before 
  preaching it.

## Instruction files **[PROVEN]**

- Copilot CLI reads `AGENTS.md` natively, plus `.github/muse-instructions.md`, 
  `.github/instructions/**/*.instructions.md` (when `applyTo` matches), root 
  `CLAUDE.md`/`GEMINI.md`, and user-level `$HOME/.copilot/copilot-instructions.md`.
- **CLI combines everything with NO defined precedence order** (github.com 
  surfaces have a precedence list; the CLI is not github.com). Don't write 
  conflicting rules and expect a referee.
- `/instructions` lists what the session loaded and lets you toggle files. 
  Edits mid-session are NOT picked up — restart or `/new`.
- Path-specific `*.instructions.md` support varies by surface; anything every 
  surface must see belongs in `.github/muse-instructions.md`.

## Sessions, skills, MCP (observed on this machine, v1.0.89)

- CLI exposes `sessions`, `memories`, `plugin`, `mcp`, `skill`, `instruction`, 
  `lsp`, `workflow` subcommands.
- Skills discovered from `.github/skills/`, `.agents/skills/`, `.claude/skills/`, 
  `~/.copilot/skills/`, `~/.agents/skills/` — note `.claude/skills/` overlap with 
  Claude Code, which this workspace's adapter exploits.
- MCP config: `~/.copilot/mcp-config.json`, `.mcp.json`, `.github/mcp.json`, plugins.
- Live discovery of *this workspace's* installed skills/agents: UNVERIFIABLE 
  until authenticated (eval E1).
