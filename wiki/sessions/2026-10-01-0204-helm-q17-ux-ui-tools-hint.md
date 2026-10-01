---
session_id: 2026-10-01-0204-helm-q17-ux-ui-tools-hint
tool: helm (fleet worker, Claude Code harness)
model: claude-opus (fleet)
started: 2026-10-01 02:04 ET
status: partial
intent: Q17 — fix the X4 defect: ux-ui agent's tools_hint grants no MCP tools, so it cannot run the Playwright browser-verification loop its own rules require.
---

# Session: Q17 ux-ui tools_hint MCP fix

## Intent
Extend the canonical ux-ui agent with an MCP grant for the Playwright
server, in the minimal schema-supported form, and verify at install
level (emitted allowlist) plus one behavioral probe (tools loaded +
one browser_navigate call by the agent).

## Starting state
- Master 1f6261b. X4 verdict REFUTED on branch lab/x4-ux-ui-loop
  @ 97ce661 (evidence evals/results/2026-10-01-X4-ux-ui-loop.md):
  arm B (ux-ui agent) loaded 4 tools (Read, Write, Edit, Bash) from
  canonical tools_hint [read, edit, shell]; zero Playwright calls;
  base arm loaded 30 tools and closed the loop. MCP config identical
  in both trees.
- adapters.py maps only read/search/shell/edit; an `mcp:` named-server
  hint form does not exist yet — the fix must add it to the translator
  (Claude: mcp__<server>__*; Copilot: <server>/*), not just the agent.

## Turn log

### 02:04 — canonical + translator change
- **Intended:** minimal schema-supported MCP grant.
- **Tried:** canonical/agents/ux-ui.md tools_hint ->
  [read, edit, shell, mcp:playwright]; scripts/adapters.py
  translate_tools_hint now accepts `mcp:<server>` tokens (validated
  server name, per-tool mcp_format rendering), callers pass
  "mcp__{server}__*" (Claude) and "{server}/*" (Copilot); comment
  block documents the form and the X4 mechanism.
- **Happened:** edits applied; adapters.py syntax OK.

### 02:10 — install-level verification
- **Intended:** emitted ux-ui allowlist carries the Playwright MCP grant; no other agent changes; guards intact.
- **Tried:** `./scripts/install.sh` with scratch HOME, twice; negative tests in a scratch copy (planted `teleport` hint; malformed `mcp:Bad_Name`).
- **Happened:** install exit 0 twice. Emitted `.claude/agents/ux-ui.md`: `tools: [Read, Write, Edit, Bash, mcp__playwright__*]`; Copilot `.github/agents/ux-ui.agent.md`: `tools: [read, edit, shell, playwright/*]`. Both negative tests abort exit 1 with named errors. PROVEN (install level).

### 02:15 — behavioral probe
- **Intended:** one `--agent ux-ui` Haiku session (X4 runner flags/config) showing playwright tools loaded + one `browser_navigate`.
- **Tried:** two attempts, scratch project `~/workspace/w6-q17-scratch/proj/` (X4 fixture, fixed emitted agent file, X4 scratch `.mcp.json`, apiKeyHelper settings).
- **Happened:** both attempts died on the first model turn, result text "Credit balance is too low" (Anthropic API account out of credit), exit 1, zero tool calls, $0 metered. Behavioral leg UNVERIFIABLE — external blocker, not evidence against the fix. Retest owed once the API account is funded.

## Learned
- The tools_hint schema had no MCP form at all: fixing an agent's MCP access is a translator change (new `mcp:<server>` token), not just a canonical edit. Any future agent needing MCP tools uses the same token.
- A Claude Code session that fails on API credit still emits an init event, but its tool list is not evidence about the agent's allowlist — the failure is upstream of tool loading.

## Outcome
partial — canonical fix + install-level verification PROVEN and committed on `fix/ux-ui-tools-hint`; behavioral probe UNVERIFIABLE (API credit exhausted, $0 spent). Remaining: X4 arm-B retest with the fixed agent (~$0.05 by X4 calibration) once the Anthropic API account is funded.
