---
session_id: 2026-10-01-0013-helm-s24-copilot-user-mcp
tool: helm
model: coordinator + 2 worker subagents
started: 2026-10-01 00:13 EDT
status: complete
intent: Close the S24 delivery gap — installer emits Copilot user-scope ~/.copilot/mcp-config.json from canonical MCP definitions, live-verified.
---

# Session: S24 Copilot user-scope MCP emission

## Intent
Ledger S24 (2026-09-30): Copilot workspace MCP is REFUTED on CLI 1.0.89;
the only working scope is user `~/.copilot/mcp-config.json`, which the
canonical installer did not emit. Close that gap with S23 safety
semantics and verify live.

## Starting state
Master `ce0edbe` (public). Branch `fix/s24-copilot-user-mcp` in
worktree `~/workspace/w1-s24-work`. Evidence base:
`docs/install-scopes-2026-09-30.md` §1c + fleet W3 findings (native
writer format verbatim, live pong from two projects).

## Turn log

### 00:1x — Builder (worker subagent)
- **Intended:** implement the emission in `scripts/adapters.py`.
- **Tried:** new `copilot_mcp_path()` / `load_existing_copilot_mcp()` /
  `copilot_user_server()`; `install_mcp()` merges into the user config;
  validation in `main()` before any write; safe outside-ROOT print in
  `write_with_backup()`.
- **Happened:** scratch tests a–e all pass — fresh format correct,
  re-run byte-identical with zero backups, seeded unrelated key/server
  preserved with byte-equal backup, malformed (3 variants) aborts exit
  1 before any write, repo gate exit 0 with only `adapters.py` modified.

### 00:4x — Verifier (independent worker subagent)
- **Intended:** reproduce from a fresh scratch HOME; live pong from
  two scratch projects.
- **Tried:** installer run, `copilot mcp list` from projA/projB,
  headless Copilot sessions calling filesystem-wiki
  `list_allowed_directories`.
- **Happened:** PROVEN on all checks — both projects return the
  absolute wiki path from the installer-emitted user-scope config.
  Auth under scratch HOME required copying `~/.config/gh/hosts.yml`
  (gh auth, not `.copilot/config.json`). Cold-cache deviation logged
  (local `_npx` cache copy after a stalled 600s network warm-up).

## Learned
- Copilot CLI auth for headless sessions resolves through `gh`
  (`~/.config/gh/hosts.yml`); a scratch HOME without it fails with
  "No authentication information found" even with `.copilot/config.json`
  present.
- Relative canonical args need install-time absolutization when the
  target scope is user-level; workspace scope keeps them relative.

## Outcome
Complete. Ledger S13 scope corrected (closure note), S24 delivery gap
closed (workspace REFUTED verdict unchanged), README gap note removed.
Evidence: `evals/results/2026-10-01-S24-copilot-user-mcp.md`.
Spend: metered $ UNVERIFIABLE (Copilot subscription sessions emitted
no $ figure; 6 `-p` attempts + 2 lists). Agents spawned: 2 workers.
