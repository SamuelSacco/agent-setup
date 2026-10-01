# Setup — follow along

Goal: from zero to both agents working off one root in ~15 minutes.

## 1. Install the tools

```bash
# Claude Code (see https://code.claude.com for the current installer)
# Version floor: >= 2.1.277. This repo ships no CLAUDE.md; AGENTS.md loads
# natively only on >= 2.1.277 when no CLAUDE.md exists. Older versions
# silently load nothing.
claude --version

# GitHub Copilot CLI
copilot --version
```

## 2. Authenticate (one human step each — do not share credentials)

```bash
claude auth login     # follow the browser/device flow
copilot login         # GitHub device flow (gh auth alone is NOT sufficient)
```

Verify:
```bash
claude auth status    # loggedIn: true
copilot               # launches and shows the signed-in GitHub account;
                      # there is no `copilot auth status` subcommand
```

## 3. Get this workspace

```bash
git clone https://github.com/SamuelSacco/agent-setup agent-setup
cd agent-setup            # <- always launch agents from here
```

One-command path: `./scripts/quickstart.sh` runs preflight, install, and
structural verify; `--structural-only` stops before the live probes (no
auth, no API spend).

Check the AGENTS.md load guard:

```bash
./scripts/check-agents-md-load.sh --static   # free: version floor + bridge check
```

The full run adds a live probe (one Haiku call). The probe authenticates
through an apiKeyHelper script: set `AGENTS_MD_LOAD_API_KEY_HELPER` to its
path (legacy alias: `CLAUDE_API_KEY_HELPER`), or pass
`--api-key-helper <path>`. With no helper configured the live probe is
skipped with a message naming the variable; the static checks still run.

## 4. Install capabilities into both tools

```bash
./scripts/install.sh
```

This reads `canonical/` and writes each tool's native layout. Add a skill 
later = one new file in `canonical/skills/` + re-run this script.

Everything it writes, including outside this repo:

- `.claude/`, `.github/`, `.mcp.json` in the repo root (adapter-owned;
  regenerated on every install).
- `~/.copilot/mcp-config.json` in your home directory — the user scope
  Copilot CLI actually loads (ledger S24; the workspace files above are
  not loaded by the CLI). It is **merged, never replaced**: unrelated
  keys and servers survive, canonical servers are replaced, and a
  changed file is first backed up to `mcp-config.json.bak-<timestamp>`
  next to the original. Two consequences to know before you run it:
  the 5 canonical servers load in **every** Copilot session on this
  machine, from any directory; and if you install from a second clone,
  the last install wins for the canonical entries (their filesystem
  paths point into that clone). There is no uninstaller yet — delete
  the canonical entries from the file by hand to remove them.
- The `github` server ships with an empty token placeholder, which the
  installer drops at emission so it cannot override a token you exported
  in your shell. Authenticated GitHub operations stay off until you set
  `GITHUB_PERSONAL_ACCESS_TOKEN` in `canonical/mcp/github.json` and
  re-run install; unauthenticated public search works either way.

## 5. First session

```bash
claude       # or: copilot
```

Ask: "Orient per AGENTS.md, then tell me what this workspace is."

Expected: the agent reads `wiki/index.md`, creates a session file under 
`wiki/sessions/`, and can explain the layout. If it doesn't, the root 
instructions didn't load — check you launched from the repo root.

## 6. Prove it (don't trust it)

First: `./scripts/quickstart.sh --structural-only` — exit 0 requires
every canonical skill and agent materialized per tool (counts derived
from `canonical/` at runtime — 9 skills and 12 agents as of 2026-10-01),
every emitted frontmatter block parsing as strict YAML, and the MCP
configs parsing (5 servers each, including the Copilot user-scope
config in `~/.copilot/`).

Then run the evals in order as auth allows: E1 (install parity) → E4 (failure 
capture) → E2 (cross-tool continuity). Record verdicts in 
`docs/claims-ledger.md`. Status (2026-09-30): E1/E2 outcomes are recorded in the ledger as S1/S2 — PROVEN at scoped wording (see their audit notes); the ledger, not this checklist, is the live definition of "done."

## 7. Headless / unattended runs

No prompt is available headless, so permissions must be granted up front.
Flag sets used by `scripts/run_eval.py`:

Claude Code:

```bash
claude -p "<prompt>" --output-format json \
  --permission-mode acceptEdits \
  --allowedTools "Write Edit Bash Read Glob Grep"
```

- `acceptEdits` + `--allowedTools` is the working set. Add tool names to
  the list as the task needs them (e.g. `Skill`).
- Do not substitute `--dangerously-skip-permissions`: it is refused when
  running as root/sudo (`--dangerously-skip-permissions cannot be used
  with root/sudo privileges for security reasons`).

GitHub Copilot CLI:

```bash
COPILOT_ALLOW_ALL=true copilot -p "<prompt>" \
  --allow-all-tools --allow-all-paths
```

- `COPILOT_ALLOW_ALL` must be exactly `true`. `run_eval.py` sets it in the
  environment; it also trusts the working directory in non-interactive
  runs (hooks and workspace config are trust-gated).
- `--allow-all-tools` / `--allow-all-paths` are the pre-approved rerun
  flags (ledger S6b). Without them, headless write prompts are denied by
  default and no files are written.

These grant the process the invoking user's filesystem and network access.
Run them only in a tree you are willing to let the agent modify.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Skill not listed in one tool | Launched outside repo root, or adapter format drift — re-run install, then check the tool's skill path |
| Instructions ignored | Wrong root: `AGENTS.md`/`CLAUDE.md` load from the launch directory upward |
| MCP server missing in one tool | Claude reads `.mcp.json`; Copilot CLI reads `~/.copilot/mcp-config.json` (user scope — `.github/mcp.json` is NOT loaded by the CLI, ledger S24; it is kept for VS Code) — re-run install; check the server appears in the right file |
| Sessions not shared | Agent didn't follow the lifecycle — check `wiki/sessions/` for the file; reinforce via AGENTS.md §2 |
