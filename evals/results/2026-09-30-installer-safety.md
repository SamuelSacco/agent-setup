# Installer safety + MCP pinning — 2026-09-30

Branch: fix/installer-safety (off phase-2). Closes docs/copilot-critique-2026-09-30.md findings #4 (installer destroys existing user configuration) and #3 (runtime supply chain `npx -y` unpinned).

## Fix A — installer config destruction

### Before (verified in scripts/adapters.py @ phase-2)
- `install_mcp()` rewrote root `.mcp.json` and `.github/mcp.json` wholesale. No backup.
- `install_hooks()` replaced the entire `hooks` object (`settings["hooks"] = settings_hooks`).
- Malformed `.claude/settings.json`: `except json.JSONDecodeError: settings = {}` — silently reset to empty, then overwritten.
- No backup, warning, or rollback on any path.

### After (scripts/adapters.py)
- Every emitted write goes through `write_with_backup()`: if the existing file's content differs, it is copied to `<file>.bak-<YYYYMMDD-HHMMSS>` next to the original (one timestamp per run) before the write. Identical content is not rewritten and creates no backup — re-running install on a converged tree is a no-op.
- `.claude/settings.json` is merged, never replaced: parsed once in `main()` before any write (`load_existing_settings()`); unrelated top-level keys and hook events canonical does not manage survive; managed events (PostToolUseFailure, SessionEnd) get the canonical entries.
- Malformed or non-object settings JSON: backup + `sys.exit` naming the file and the backup path, before anything is written. Same treatment if the existing `hooks` value is not a JSON object. The silent `{}` reset is gone.
- MCP files remain wholesale-replaced: they are fully adapter-owned and hold no user keys, so replace-with-backup is the correct write. Choice recorded in a comment in `install_mcp()`.
- `.gitignore`: `*.bak-*` (backups are local rollback state, never committed).

### Verification (scratch copies, 2026-09-30)
18/18 checks passed (harness seeded real user state, not just fresh trees):

| Case | Result |
|---|---|
| Seeded settings (custom top-level key + custom PreToolUse hook + stale managed entry) | exit 0; custom key survives verbatim; PreToolUse survives; PostToolUseFailure replaced with canonical; SessionEnd added |
| Sentinel `.mcp.json` (`{"sentinel": 1}`) | replaced; `.mcp.json.bak-<ts>` holds the sentinel content |
| Settings backup | `settings.json.bak-<ts>` holds the exact seeded document |
| Re-run on converged tree | exit 0; backup count unchanged (no-op) |
| Malformed settings (`{not json`) | exit 1; error names the file and the backup path; backup holds the malformed bytes; `.mcp.json` untouched, no `.mcp.json` backup (abort precedes all writes) |
| Non-object settings (`["a","list"]`) | exit 1 + backup |
| Fresh empty tree (canonical/ + scripts/ only) | exit 0; zero backups; emitted files created |
| Repo self-install | exit 0; backups created for exactly the two files the pin change altered (`.mcp.json`, `.github/mcp.json`); `git status` shows only intended changes (backups gitignored; removed from this tree after verification) |

## Fix B — MCP supply chain pinning

All five canonical servers were `npx -y` with bare or `@latest` specs. Now pinned to exact versions. Versions retrieved 2026-09-30 from the npm registry `/latest` endpoint and cross-checked with `npm view <pkg> version` (both methods agreed on all five):

| Server | Canonical file | Before | Pinned |
|---|---|---|---|
| context7 | canonical/mcp/context7.json | `@upstash/context7-mcp@latest` | `@upstash/context7-mcp@4.1.1` |
| filesystem-wiki | canonical/mcp/filesystem-wiki.json | `@modelcontextprotocol/server-filesystem` | `@modelcontextprotocol/server-filesystem@2026.8.31` |
| github | canonical/mcp/github.json | `@modelcontextprotocol/server-github` | `@modelcontextprotocol/server-github@2025.4.8` |
| playwright | canonical/mcp/playwright.json | `@playwright/mcp` | `@playwright/mcp@0.0.83` |
| sequential-thinking | canonical/mcp/sequential-thinking.json | `@modelcontextprotocol/server-sequential-thinking` | `@modelcontextprotocol/server-sequential-thinking@2026.8.31` |

All five are npm-based; none left unpinned. Mirrors regenerated via `scripts/install.sh`; canonical and emitted configs committed together.

### Verification
- `grep` over canonical/mcp/*.json: every package spec carries an exact version (no `@latest`, no bare spec). Same in emitted `.mcp.json` and `.github/mcp.json`.
- Structural verify (quickstart.sh §3 checks, run verbatim): PASS — claude skills 8/8, copilot skills 8/8, claude agents 12/12, copilot agents 12/12, both MCP configs parse with 5 servers.
- Live smoke: `npx -y @modelcontextprotocol/server-sequential-thinking@2026.8.31` launched and answered MCP `initialize` (serverInfo: `sequential-thinking-server`, version `2026.8.31` — the pinned version reporting itself) and `tools/list` (`sequentialthinking`). PASS.
- Caveats: first cold-cache launch in this sandbox exceeded a 120 s window before succeeding on a subsequent attempt (~38 s diag run; ~5 s warm). Consistent with the known cold-npx-cache caveat (S14). Playwright not smoke-launched — root-sandbox carve-out (S14, PARTIAL there). Remaining four pins verified at the registry + config level, not individually launched.
- Version freshness is as of 2026-09-30. Pinning trades trust-latest for staleness: bump deliberately by editing canonical/mcp/*.json and re-running install; there is no auto-update path, by design.

## Verdicts
- Fix A: **PROVEN** (scratch behavioral, 18/18; repo self-install clean).
- Fix B: **PROVEN** (pinning complete in canonical + mirrors; one pinned server launched and answered at the pinned version; other servers PROVEN at registry/config level, launch UNVERIFIABLE here beyond sequential-thinking).

Spend: $0 (registry reads + local runs; no model calls).
