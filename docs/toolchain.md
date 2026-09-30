# Organizational Toolchain

How the work toolchain plugs into this setup. Each tool enters through the 
same capability layer (`canonical/`), so it works in both coding agents.

> Verification status: entries describe the integration *mechanism*. Live 
> verification against org accounts is UNVERIFIABLE from this workspace — 
> run the check in the right column before presenting it as working.

| Tool | Mechanism | Canonical home | Verify by |
|------|-----------|----------------|-----------|
| GitLab CLI (`glab`) | CLI + skill wrapping common flows (MRs, CI) | `canonical/skills/gitlab.md` (planned — not yet authored) | `glab auth status`; open a test MR |
| Coralogix | MCP server (logs/traces queries) | `canonical/mcp/coralogix.json` (planned — not yet authored) | MCP handshake; one log query per tool |
| MongoDB | `mongosh` via shell; optional MCP server | `canonical/mcp/mongodb.json` | `mongosh --eval 'db.runCommand({ping:1})'` |
| Postgres | `psql` via shell | (shell skill) `canonical/skills/db-shell.md` | `psql -c 'select 1'` |
| Okteto | CLI skill (deploy/dev endpoints) | `canonical/skills/okteto.md` | `okteto version`; `okteto list` |
| Atlassian (Jira/Confluence) | MCP server (official Atlassian MCP) | `canonical/mcp/atlassian.json` (planned — not yet authored) | MCP handshake; fetch one known ticket |
| Chrome DevTools | MCP server (`chrome-devtools-mcp`) | `canonical/mcp/chrome-devtools.json` | Open a page, read console/network via MCP |
| CodeRabbit | PR-review integration + skill for acting on reviews | `canonical/skills/coderabbit.md` | Open a PR; confirm review appears |
| Figma | MCP server (official Figma MCP) | `canonical/mcp/figma.json` | Fetch one frame's structure via MCP |

## Pattern to teach

Every row is the same move: **define once in `canonical/`, install with 
`./scripts/install.sh`, verify with the check.** New tool joins the org? It's a 
new canonical file, not a new per-agent setup ritual. That is the whole pitch 
for the adapter layer.

## Auth rules

- API keys/tokens go in each tool's secure config or env — never in `canonical/` 
  and never committed.
- Prefer OAuth/device flows over pasted keys.
- One person's credentials are never shared between tools or people.
