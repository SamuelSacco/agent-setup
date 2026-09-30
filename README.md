# Agent Setup — Tool-Agnostic Coding Agent System

A sterile, reproducible setup for running **Claude Code** and **GitHub Copilot CLI** 
from one shared root, with one-install capabilities, a self-maintaining knowledge wiki, 
normalized session telemetry, and lifecycle evaluations.

Nothing here is personal. Clone it, run the installer, and both tools behave the same.

## Quick start

```bash
# 1. Clone and enter the root (always launch agents from here)
cd agent-setup

# 2. Install capabilities into both tools (one command)
./scripts/install.sh

# 3. Launch either tool from this directory
claude          # Claude Code
copilot         # GitHub Copilot CLI
```

Both tools read the same `AGENTS.md`, share the same skills/agents/MCP servers via 
adapters, write sessions into `wiki/sessions/`, and maintain the wiki in `wiki/notes/`.

## Layout

```
agent-setup/
├── AGENTS.md              # Root instructions both tools load (the schema)
├── .github/
│   └── muse-instructions.md   # Copilot-specific pointer → AGENTS.md
├── canonical/             # Provider-neutral definitions (source of truth)
│   ├── skills/            #   skill definitions (name, description, body)
│   ├── agents/            #   specialist agent definitions
│   ├── mcp/               #   MCP server definitions
│   ├── hooks/             #   lifecycle hook definitions
│   └── plugins/           #   plugin bundle definitions
├── adapters/              # Generated per-tool files (do not edit by hand)
│   ├── claude/            #   .claude/ layout for Claude Code
│   └── copilot/           #   .github/ + ~/.copilot layout for Copilot CLI
├── wiki/                  # The knowledge system (Karpathy llm-wiki pattern)
│   ├── raw/               #   Immutable sources (never edited by agents)
│   ├── notes/             #   LLM-maintained linked Markdown (YAML frontmatter)
│   ├── sessions/          #   Append-only session logs (audit trail)
│   ├── index.md           #   Map of notes
│   └── log.md             #   Append-only change log
├── evals/                 # Controlled evaluations
│   ├── tasks/             #   Task definitions with baselines
│   └── results/           #   Run results (PROVEN / REFUTED / UNVERIFIABLE)
├── scripts/               # install.sh, adapters, sidecar, eval runner
└── docs/                  # Setup guide, toolchain, tips & tricks
```

## Principles

1. **One install, both tools.** Define a capability once in `canonical/`; adapters 
   materialize each tool's native format. Never hand-maintain two copies.
2. **Evidence over claims.** Every feature claim carries a verdict: PROVEN, REFUTED, 
   or UNVERIFIABLE, backed by a controlled test in `evals/`.
3. **The wiki is the memory.** Agents orient from `wiki/index.md`, log every session, 
   and harden raw session material into maintained notes at session end.
4. **Telemetry without context bloat.** Hooks and OTEL go to a sidecar store 
   (JSONL/SQLite); only summaries enter the prompt.
5. **Lightweight.** This is the slim version of the ECC-style kitchen sink: 
   the minimum that demonstrably helps, measured.

## Status

See `docs/claims-ledger.md` for the live verdict on every claim this system makes.
