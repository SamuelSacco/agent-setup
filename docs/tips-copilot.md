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
  *(Docs-PROVEN. Local caveat 2026-09-30: `copilot instruction list` does not 
  enumerate the muse-instructions.md source — isolated-dir test finds nothing. 
  Authenticated probe pending; our setup doesn't depend on it.)*
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
- Live discovery of *this workspace's* installed skills/agents: PROVEN
  2026-09-30 (E1 — Copilot invoked `session-harden` by name in a fresh
  install and executed its body).

## Hooks **[documented; REFUTED on installed v1.0.89]**

- GitHub documents repo hooks in `.github/hooks/*.json` (14 events incl.
  `postToolUseFailure`, user-level `~/.copilot/hooks/*.json` too). Our E4
  test: 0/5 induced failures captured; no hook has ever fired in this
  machine's session logs. Docs ≠ shipped — don't build on repo hooks on
  this build. The SDK extension-API hook path exists but is untested.

## Telemetry **[PROVEN live 2026-09-30]**

- `COPILOT_OTEL_FILE_EXPORTER_PATH=<file>` alone enables OTel and selects
  the file exporter (traces + metrics as JSONL). Add
  `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` for full
  prompts, system instructions, and tool definitions in the spans.
- Exporter is file **xor** `otlp-http` per process — one sink only.
  `copilot help monitoring` is the full local reference.
- First debugging question for any "why did that cost so much": read the
  `chat` span — system instructions and every tool schema are itemized.

## Same-key BYOK **[PROVEN]**

- `COPILOT_PROVIDER_TYPE=anthropic` + base URL + API key + model ID runs
  Copilot on your Anthropic key: model constant, harness the only variable.
  Usage meters in tokens, no AI Credits line.

## Custom agents — verify the disk, not the summary

- E6 pilot (2026-09-30): `copilot --agent backend` accepted the agent,
  ran ~4 min, and reported "22 passed, production-ready" while writing
  **zero files** (`Changes +0 -0`); the quoted test transcript was
  fabricated. After any agent run, check the artifacts exist before
  believing the summary.
