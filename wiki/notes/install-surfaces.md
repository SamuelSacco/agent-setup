---
id: install-surfaces
title: Install surfaces — how capabilities actually reach each CLI (P2 W1)
type: reference
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [instruction-files, session-lifecycle]
sources: []
tags: [install, skills, plugins, mcp, copilot, claude]
---

Measured 2026-09-30 (P2 W1, `evals/results/2026-09-30-P2-install-matrix.md`);
every cell proven by invocation, fixtures in `evals/fixtures/w1-install-probes/`.

- **`npx skills add` is skills-only.** Canonical copy in `.agents/skills/`,
  per-agent symlinks (`.claude/skills/<n> -> ../../.agents/skills/<n>`),
  `skills-lock.json`. Copilot reads `.agents/skills/` natively — no
  Copilot-specific file is written. Agents/hooks/MCP/plugins: no such path.
- **One plugin tree serves both tools.** `.claude-plugin/plugin.json` +
  `skills/`, `agents/`, `hooks/hooks.json`, `.mcp.json`: Claude installs via
  local marketplace; Copilot via local path (deprecation warning) or its
  marketplace. Bundled skill/agent/MCP/hook all fired in both. Copilot's
  install summary under-reports what works.
- **Copilot workspace config is trust-gated invisibly.** Without
  `COPILOT_ALLOW_ALL=true`, `copilot mcp list` says "No MCP servers
  configured" with correct files on disk. `copilot mcp add` also refuses
  group/other-writable config dirs (`chmod 700` fixes).
- **Copilot MCP key is `mcpServers`, also in `.github/mcp.json`.** A
  `{"servers": …}`-only file is rejected as malformed. Adapter fixed
  2026-09-30 to emit both keys (`scripts/adapters.py`, commit 4ed071c).
