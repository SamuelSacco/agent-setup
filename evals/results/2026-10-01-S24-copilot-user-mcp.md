# S24 closure — installer emits Copilot user-scope MCP config

Date: 2026-10-01 ET. Branch `fix/s24-copilot-user-mcp` off master `ce0edbe`.
Closes the delivery gap recorded in ledger S24 / S13 scope correction
(2026-09-30): the canonical install did not emit the only Copilot MCP
scope that loads on CLI 1.0.89.

## Change

`scripts/adapters.py` — `install_mcp()` now also writes the Copilot
user-scope config `~/.copilot/mcp-config.json` (`Path.home()`, honours
`$HOME`) from the same canonical servers dict built from
`canonical/mcp/*.json` that feeds Claude's `.mcp.json`:

- Per-server entry in Copilot's own writer format (fleet evidence,
  `docs/install-scopes-2026-09-30.md` §1c): `{"type": "local",
  "command", "args", "tools": ["*"]}`, plus `"env"` only when the
  canonical env is non-empty.
- Relative path args (`./`, `../`) resolve to absolute paths against
  the repo root for this emission only — user-scope sessions run from
  arbitrary cwds, so `./wiki` (filesystem-wiki) must not depend on cwd.
  Workspace emissions unchanged.
- The user config is user-owned: merged, never replaced (unrelated
  top-level keys and non-canonical servers preserved; canonical-named
  entries replaced). Writes go through `write_with_backup()`
  (timestamped backup on change, no-op when identical).
- Malformed existing config (invalid JSON, non-object top level,
  non-object `mcpServers`) aborts the install before any write:
  original backed up, error names file + backup path. Same semantics
  as `.claude/settings.json` (ledger S23). Never reset to `{}`.
- Workspace `.github/mcp.json` emission kept (VS Code consumers, future
  Copilot); the workspace scope itself remains REFUTED on 1.0.89.

## Verification

Builder scratch tests (scratch HOME, logs in
`~/workspace/w1-s24-scratch/`):

- Fresh install: exit 0; emitted config parses; all 5 canonical servers
  present, `type: "local"`, `tools: ["*"]`; filesystem-wiki args carry
  the absolute worktree wiki path; `env` only on github.
- Convergence: second run byte-identical (sha256 match), zero backups.
- Preservation: seeded unrelated top-level key + non-canonical server
  survive; backup of the seeded file created, byte-equal to the seed.
- Malformed: invalid JSON → exit 1, error names file + backup, seeded
  content preserved in backup, every pre-existing workspace file
  unchanged by hash and mtime. Non-object top level and non-object
  `mcpServers` variants: same abort behavior.
- Repo gate: `./scripts/install.sh` exit 0 in the worktree; `git
  status` shows only the `adapters.py` edit.

Independent verifier (fresh scratch HOME `~/workspace/w1-s24-verify/`,
raw outputs there):

- Fresh install reproduced: exit 0, assertion pass on all 5 servers
  and format.
- `copilot mcp list` from two empty scratch projects: all 5 servers
  listed as User servers (local), exit 0 from both cwds.
- **Live pong PROVEN from both projects**: headless Copilot sessions
  (`COPILOT_ALLOW_ALL=true`, `--allow-all-tools --allow-all-paths`)
  instructed to call filesystem-wiki's `list_allowed_directories`
  returned exactly the absolute wiki path from projA and from projB.
  That string is emitted only by the server executing, so the
  installer-emitted user-scope config loaded and ran from both cwds.
  Session logs show all 5 servers initialized (filesystem 0.2.0,
  sequential-thinking 2026.8.31, Context7 4.1.1, Playwright, github
  0.6.2).

## Findings

- **Copilot auth under a scratch HOME is `gh`, not `.copilot`.** First
  sessions failed `Error: No authentication information found.`;
  copying `~/.copilot/config.json` did not fix it. Copying
  `~/.config/gh/hosts.yml` + `config.yml` (file copy only; values never
  read) did. Scratch-HOME Copilot verification requires the gh auth
  files present.
- Cold npm cache under a scratch HOME exceeded Copilot's 60s MCP
  lifecycle cap (one session: "No tools were available for
  filesystem-wiki"). The verifier completed the scratch `_npx` cache
  by local disk copy of the identical package trees from the real
  HOME cache after a prescribed 600s network warm-up stalled on a
  throttled network (deviation logged in
  `~/workspace/w1-s24-verify/raw/check3-cache-warm-deviation.txt`).
  After that, the server starts in ~2s and Copilot spawned/executed
  everything itself from the installer-emitted config. Same class as
  the S14/S23 cold-cache caveat; warm-cache behavior unaffected.
- `copilot --version` prints 1.0.90; runtime logs report
  `client_version=1.0.89` / `copilot_runtime_version=1.0.89`. The S24
  verdicts were recorded against the 1.0.89 runtime.

## Spend

Metered $ UNVERIFIABLE: 6 Copilot `-p` attempts + 2 `mcp list` runs,
all subscription-billed with `-s`; the CLI emitted no dollar or
AI-credits figure in any output. No Claude model calls.
