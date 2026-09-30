---
session_id: 2026-09-30-1512-helm-installer-safety
tool: claude-code
model: Muse Spark (helm subagent)
started: 2026-09-30 15:12 EDT
status: complete
intent: Fix installer config destruction (no backup/rollback, silent {} reset) and unpinned npx MCP supply chain — copilot-critique findings #4 and #3.
---

# Session: Installer safety + MCP pinning

## Intent
Samuel's repo-hardening program: fix docs/copilot-critique-2026-09-30.md findings #3 (runtime supply chain `npx -y` unpinned) and #4 (installer destroys existing user configuration) on branch fix/installer-safety off origin/phase-2. Disk-verify, commit, push.

## Starting state
- phase-2 @ a3506dc (S21 merged). Ledger ID space: S1–S21 used; next free = S22.
- Verified on disk before editing: install_mcp() rewrites .mcp.json + .github/mcp.json wholesale, no backup; install_hooks() does settings["hooks"] = settings_hooks and `except json.JSONDecodeError: settings = {}` (silent reset, adapters.py). All five canonical/mcp/*.json use `npx -y` with bare or @latest specs.

## Turn log

### 15:12 — clone + audit
- **Intended:** fresh clone, own branch, verify critique claims against code.
- **Tried:** git clone from ~/workspace/agent-setup, branch fix/installer-safety off origin/phase-2; read adapters.py, install.sh, canonical/mcp/*.json, claims-ledger tail.
- **Happened:** both findings CONFIRMED as written. npm registry version lookup launched.

### 15:14 — Fix A implemented + scratch-verified
- **Intended:** backup-on-change for all emitted writes; settings merged; malformed settings fail loud before any write.
- **Tried:** adapters.py: write_with_backup()/backup_file()/load_existing_settings() helpers; settings parsed once in main() preflight; install_hooks() merges (unmanaged hook events + unrelated keys survive); MCP wholesale-replace-with-backup choice commented in code; *.bak-* gitignored. Scratch harness with seeded user state.
- **Happened:** 18/18 checks PASS — seeded custom key + custom PreToolUse hook survive; sentinel backups hold prior content; malformed settings exits 1, original preserved, .mcp.json untouched (abort precedes writes); non-object settings same; fresh tree zero backups; re-run no-op.

### 15:20 — Fix B: MCP pinning + live smoke
- **Intended:** pin all five canonical MCP specs to exact registry versions; regenerate; smoke-launch one pinned server.
- **Tried:** npm registry /latest cross-checked with npm view (agreed on all five); sed pins into canonical/mcp/*.json; ./scripts/install.sh; structural verify block from quickstart.sh §3 run verbatim; stdio JSON-RPC smoke against the pinned sequential-thinking spec.
- **Happened:** pins — context7 4.1.1, filesystem 2026.8.31, github 2025.4.8, playwright-mcp 0.0.83, sequential-thinking 2026.8.31. Structural PASS (8/8, 12/12, 5+5 servers parse). Smoke PASS: initialize returns serverInfo version 2026.8.31; tools/list = [sequentialthinking]. First cold-cache launch exceeded 120 s (known S14-class caveat); warm ~5 s. Repo self-install created backups for exactly the two pin-changed files; removed after verification (gitignored).

## Learned
- write_with_backup with a shared per-run timestamp makes install idempotent AND auditable: converged tree = zero writes, zero backups.
- The settings file is the only user-owned emitted file; everything else is adapter-owned, where replace-with-backup is the correct semantics. The distinction belongs in code comments.
- npx cold-cache latency in this sandbox can exceed 120 s for an MCP server's first launch; warm launches are seconds. Verdicts must state which.

## Outcome
complete — both fixes PROVEN at the scopes recorded in evals/results/2026-09-30-installer-safety.md and ledger S23 (numbered S22 on the branch; renumbered at merge — S22 is the Opus-tier claim). Branch fix/installer-safety pushed.
