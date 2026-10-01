# Install scopes: skills, plugins, MCP servers — mechanics + organization model

Date: 2026-09-30 ET. Sources: live probes on skills CLI 1.7.0, Claude Code 2.1.285 (self-updated to 2.1.286 mid-run; no behavior differences observed), Copilot CLI 1.0.89. Evidence discipline: PROVEN = live probe; DOCS-ONLY = from help/docs text; REFUTED = probed and absent; UNVERIFIABLE = blocked. Full evidence: `~/workspace/p3/install-scopes/findings/w1-skills.md`, `w2-plugins.md`, `w3-mcp.md`; debate `w4-paper-global.md`, `w4-paper-project.md`; judgment `w4-judgment.md`.

## 1. Verified mechanics

### 1a. Skills (`npx skills add dbos-inc/agent-skills`)
- **One canonical store + symlinks, not copies.** Global: real files in `~/.agents/skills/<name>`; symlinks fanned out into 56 agent dirs incl. `~/.claude/skills`; 23 "universal" agents (incl. Copilot project scope) read the canonical dir directly. Project: `./.agents/skills/<name>` + one `./.claude/skills` symlink + `./skills-lock.json`. (PROVEN)
- **Claude discovery = `.claude/skills` paths only.** Direct read of `~/.agents/skills` by Claude is REFUTED — Claude sees these skills only via the symlinks the CLI creates (global `~/.claude/skills`, project `.claude/skills`). **Copilot** discovers `~/.copilot/skills`, `~/.agents/skills`, and project `.github/skills`, `.agents/skills`, `.claude/skills`. (all PROVEN)
- **Collision rule inverts by tool.** Same skill name in global and project: Claude runs the **global** one (PROVEN — probe returned the global body), Copilot's list shows the **project** entry. (PROVEN)
- **Flags that matter:** `-g/--global` (default is project), `-a/--agent <names|*>` (registry of 79 agents; without it, `-y` fans out to all ~56 symlink dirs), `-y/--yes` (required for automation — the interactive scope prompt defaults to Project and blocks non-TTY), `-s/--skill`, `--all` (= `-s '*' -a '*' -y`), `--copy` (copies instead of symlinks; **PROVEN 2026-10-01, X16/S27** — real dirs in canonical + `~/.claude/skills`, content byte-identical to source, Copilot served via canonical store). `remove`/`update`/`list` mirror `-g/-a/-y/--json`.
- **Locks are hash-only, no version.** Global `~/.agents/.skill-lock.json` records per-skill `skillFolderHash`, source URL — no commit SHA, no tag. `update -g -y` re-contacts GitHub and re-fans out. (PROVEN)
- **Removal** (`skills remove [-g] <name> -y`) deletes the canonical dir, all symlinks, and the lock entry. (PROVEN)

### 1b. Plugins
- **Claude:** `claude plugin {marketplace add,list,remove,update, install,uninstall,enable,disable,list,details,update,validate}` — fully automatable, interactive `/plugin` UI never needed. Payloads are **scope-independent**: one shared cache at `~/.claude/plugins/cache/<mkt>/<plugin>/<version-or-git-SHA>/`; scope is only which settings file holds `enabledPlugins`: user `~/.claude/settings.json`, project `<proj>/.claude/settings.json`, local `<proj>/.claude/settings.local.json`. Registry `installed_plugins.json` records scope + projectPath. (PROVEN)
- **Visibility (live sessions):** user plugin visible inside an unrelated project's session; project plugin visible in its own project, invisible from a sibling; disabled = invisible. (all PROVEN)
- **Bundle:** `.claude-plugin/plugin.json` (name/description/author only; no version → cache keyed by git SHA); components discovered by convention — `commands/*.md` (surfaced as skills), `skills/<n>/SKILL.md`, `agents/*.md`, `hooks/hooks.json` + scripts, `.mcp.json` slot (untested — both test plugins had none; DOCS-ONLY). Always-on rent measured ~71–218 tok per small test plugin. Uninstall leaves the payload in cache (orphaned); marketplace remove cascades to uninstall its plugins. (PROVEN)
- **Copilot has a real plugin system, near-parity:** `copilot plugin {install,uninstall,update,list,enable,disable,marketplace}`, payloads at `~/.copilot/installed-plugins/<mkt>/<plugin>/`, enablement `~/.copilot/settings.json:enabledPlugins`. **No CLI scope flag** — CLI installs are user-scope only; repo-scope declaration (`.github/copilot/settings.json`) is DOCS-ONLY. Uninstall is cleaner than Claude (payload deleted, no orphan). (PROVEN for installs/enablement; session-level skill loading UNVERIFIABLE — no GitHub auth under fake HOME)
- **Cross-compat:** Copilot reads Claude-format `.claude-plugin/plugin.json` and installs Claude plugins via `--plugin-dir` or direct `owner/repo:path` (PROVEN at install/list level) — but registering the official Claude marketplace is REFUTED (schema rejects typed-object sources), and Copilot never auto-reads `~/.claude/plugins`.

### 1c. MCP servers
- **Claude scopes (PROVEN at health-check level; live tool calls UNVERIFIABLE — probe account's credit exhausted):**
  - `user`: `~/.claude.json` top-level `mcpServers` — ✔ Connected in every project, **no gate**.
  - `project`: `<proj>/.mcp.json` — project + subdirs only, ⏸ Pending approval. Pre-approval = hand-edit `projects[<path>].hasTrustDialogAccepted=true` in `~/.claude.json`; setting `enabledMcpjsonServers` alone is insufficient; **no CLI flag exists** for this.
  - `local` (the `-s` default — say the scope explicitly): `~/.claude.json` `projects[<abs path>].mcpServers` — that project only, no gate.
  - `claude mcp remove` without `-s` removes from whichever scope matches. `-e KEY=v` stores plaintext in the config file (perms `-rw-------`). Variadic-`-e` gotcha: the server name must precede `-e`, else the name is swallowed as an env value.
- **Copilot (live tool calls PROVEN):** user config `~/.copilot/mcp-config.json`, top key `mcpServers`, `type:"local"` (Claude's `stdio` is rejected by Claude with diagnostics; Copilot's own writer emits `mcpServers`/`local` only — the dual-key `servers` emission is legacy/VS Code compat, not what the CLI uses). User server returned a live pong from two different projects. `copilot mcp {add,remove,list,get,enable,disable}` are real commands; `add` targets user config only. `--env` values stored plaintext; `mcp get` masks them unless `--show-secrets`.
- **Copilot workspace MCP: REFUTED on 1.0.89.** `.mcp.json`, `.github/mcp.json`, `.vscode/mcp.json` in every key/type variant (git init or not) never appeared in `copilot mcp list` or a live session — while `copilot mcp --help` itself documents them as Workspace sources (DOCS-ONLY). This **supersedes** the earlier Phase 2 claim that Copilot listed workspace servers (older binary/evidence). Precedence: session `--additional-mcp-config` beats the user file on name conflict (last-loaded wins; PROVEN).

## 2. Scope matrix (artifact × tool × scope)

| Artifact / scope | Tool | Config path / file location | Visibility rule | Gate / notes |
|---|---|---|---|---|
| Skill · global | Claude | `~/.agents/skills/<n>` + symlink `~/.claude/skills/<n>` | every project | none |
| Skill · global | Copilot | `~/.agents/skills/<n>` (source `personal-agents`) or `~/.copilot/skills` | every project | none |
| Skill · project | Claude | `./.agents/skills/<n>` + `./.claude/skills/<n>` symlink | that project only; **global wins on name collision** | interactive scope prompt (defaults project; `-y` to skip) |
| Skill · project | Copilot | `./.agents/skills` or `./.github/skills` (source `project`) | that project only; **project wins on name collision** | same |
| Plugin · user | Claude | settings `~/.claude/settings.json`; payload shared cache | every project | none; always-on rent ~71–218 tok/small plugin |
| Plugin · project | Claude | `<proj>/.claude/settings.json` | that project only, invisible from siblings | none |
| Plugin · user | Copilot | `~/.copilot/settings.json`; payload `~/.copilot/installed-plugins/` | every session | none (session-level loading UNVERIFIABLE) |
| MCP · user | Claude | `~/.claude.json` → `mcpServers` | every project | none — the only zero-gate scope |
| MCP · project | Claude | `<proj>/.mcp.json` | that project + subdirs | ⏸ Pending approval; pre-approve via `hasTrustDialogAccepted=true` hand-edit (no CLI flag) |
| MCP · local | Claude | `~/.claude.json` → `projects[<path>].mcpServers` | that project only | none (default `-s` — say it explicitly) |
| MCP · user | Copilot | `~/.copilot/mcp-config.json` → `mcpServers` | every cwd | none — the only working Copilot scope |
| MCP · workspace | Copilot | `.mcp.json` / `.github/mcp.json` (DOCS-ONLY) | **REFUTED 1.0.89** | do not depend on it today |

## 3. Judged organization model

Verdict from the debate reconciliation: **the canonical repo is the source of truth; user/global scope is the default install target.** The project-first paper won on *where state is recorded* (reproducibility, reviewability, pinning); the global-first paper won on *where state lands* (user scope is the only scope PROVEN connected everywhere with zero gates in both tools). Neither pure position survived the probes.

| Artifact | Default | Exception | Source of truth | Transfer |
|---|---|---|---|---|
| Skills | **global** (`skills add -g --agent claude-code github-copilot`) | project scope only when content genuinely differs — **never the same name in both** (Claude global-wins is PROVEN; enforce with a name-collision lint) | canonical repo + SHA-256 pin per skill (X6 wired into install.sh) + machine-readable setup manifest of add commands | replay manifest; teammate clones + runs install |
| Plugins (Claude) | **user** | project scope for repo-specific plugins | canonical repo: marketplace declarations (source + pinned commit SHA) + per-scope `enabledPlugins` lists | `marketplace add` (pinned SHA) + `plugin install --scope user` |
| Plugins (Copilot) | **user** (CLI has no other scope) | repo-scope enablement is DOCS-ONLY — not a default until probed | same canonical record | `copilot plugin install` per manifest |
| MCP (Claude) | **user** for personal; **project `.mcp.json`** for team-shared definitions | local scope as last-resort per-machine override | canonical repo holds definitions (names, commands, env var NAMES) — **no values** | replay via add-json/manifest; one interactive approval per machine per project |
| MCP (Copilot) | **user** — the only path that loads on 1.0.89 | workspace entries may be *emitted* for a future release but are not today's delivery path | same canonical definitions | `copilot mcp add` per manifest |

Contested/accepted-with-mechanism points:
- **Secrets:** definitions in repo, values only in `~/.config/agent-setup/secrets.env` (0600, mode-verified), injected at install via `claude mcp add-json` / `copilot mcp add --env`; OAuth preferred over static keys; scheduled scan greps the repo for secret-shaped values. Residual: both CLIs store secrets plaintext on disk — the model narrows who holds them, it does not claim to encrypt them.
- **Pinning/drift:** skills pinned by SHA (X6 wiring), plugins by marketplace commit SHA, MCP by `last-verified` date; a weekly `verify` compares installed state against the canonical record — loud divergence replaces silent drift. Enforcement tooling (collision lint, secrets scan, pin wiring, weekly verify) is designed, not yet built — the model is policy until then. **Amendment 2026-10-01 (Q8, branch `feat/drift-enforcement`): collision lint, secrets scan, skill/MCP pin verification, and weekly verify are BUILT — `scripts/drift_check.py` (subcommands `collisions`/`secrets`/`pins`/`all`), `scripts/verify-weekly.sh`, self-test `scripts/test_drift_check.py` (11/11 PASS, real-repo run exit 0; evidence `evals/results/2026-10-01-Q8-drift-enforcement.md`). Pin wiring into install.sh remains a follow-up; the checks are not yet called by install.**
- **install.sh coexistence:** verified against current `adapters.py` — `write_with_backup()` timestamps every backup, `.claude/settings.json` is merged (never replaced), malformed settings abort before any write. Rule: install.sh is merge-only on shared JSON, keeps a per-key/file ownership registry, registers hand-added globals on sight (import, don't overwrite), and carries `ADAPTER-OWNED` headers on wholesale-replaced files.

### Samuel's scenarios under this model
- **At ~, no project:** skill → `npx -y skills add <repo> -g -y --agent claude-code github-copilot` (the second `-y` skips the project-defaulting scope prompt); MCP → `claude mcp add -s user` (`-s user` is mandatory — default is local) / `copilot mcp add`; plugin → `claude plugin install <n>@<mkt> --scope user` / `copilot plugin install`. Then one line in the setup manifest — the add is the install, the manifest line is what makes it reproducible.
- **Open at ~, cd into a project:** everything user-scope follows (globals listed cross-project, user plugins in foreign sessions, Claude user MCP connected everywhere, Copilot user MCP ponging from any cwd — all PROVEN). The project's own layer resolves on top; project `.mcp.json` servers appear ⏸ Pending approval until the one-time interactive trust. Nothing from *another* project follows you.
- **From project to everywhere (promotion):** try at project scope → promote to canonical (source in repo, import/audit for skills, pin commit for plugins, record definition for MCP) → commit/push → redistribute: run the global add once from anywhere and delete the project copy (`skills remove` from the project cwd, `plugin uninstall --scope project`, `claude mcp remove` auto-detects scope) so no shadow remains. If it can't be justified as "every future project pays this rent," it stays project-scoped.

### New-machine onboarding (ordered)
1. Clone the canonical repo. 2. `scripts/quickstart.sh` (1m58s cold / 30s warm, measured). 3. Authenticate both CLIs (2 unavoidable human actions). 4. Create `~/.config/agent-setup/secrets.env` (0600) once. 5. `./scripts/install.sh` (emits global + per-project layers). 6–7. Verify: `skills list -g`, `claude mcp list`, `copilot mcp list`. 8. Approve project `.mcp.json` servers once per project (interactive). 9–10. Run collision lint, secrets scan, pin `verify` — all green = clean baseline. 11. Cold-start check in a scratch project. 12. Record CLI versions in the manifest log (version-fragile behavior needs a provenance trail).

## 4. Still docs-only / unverified / contested
- Copilot repo-scope plugins (`.github/copilot/settings.json`): DOCS-ONLY, unexercised.
- skills CLI `experimental_install`/`experimental_sync` restore flow: flag surface PROVEN, restore UNVERIFIED (portability rests on re-running `add`, not lock-restore).
- Claude plugin `.mcp.json` slot: DOCS-ONLY (both test plugins shipped 0 MCP servers).
- Claude live tool calls on MCP: UNVERIFIABLE on the probe account (credit exhausted); scope cells rest on `claude mcp list` health checks.
- Claude local-scope MCP at live tool-call level: health-check PROVEN, tool-call UNVERIFIABLE.
- Copilot session-level loading of Claude-format plugin skills: install/list recognition PROVEN, in-session loading UNVERIFIABLE (auth block).
- Copilot workspace MCP: DOCS-ONLY (tool's own help) + REFUTED in probes → treated as dead on 1.0.89; re-probe on the next Copilot minor before promoting it back.
- X6 pin wiring into install.sh, name-collision lint, secrets scan, weekly verify: designed, not built.
  - **Amendment 2026-10-01 (Q8, branch `feat/drift-enforcement`): name-collision lint, secrets scan, and weekly verify BUILT (`scripts/drift_check.py`, `scripts/verify-weekly.sh`, `scripts/test_drift_check.py`); X6 pin wiring into install.sh still not built.**

## 5. Spend ledger (fleet)
- W1: $0.0377 (3 Haiku probes) + 1 GitHub-hosted Copilot probe (AI credits, not metered here).
- W2: $0.042 (4 Haiku probes + 1 failed).
- W3: $0.00 Claude (no model call succeeded), 5 Copilot subscription sessions, no $ figure emitted.
- W4 papers + judge + W5: no model calls (read/write only); W5 re-executions are CLI/file ops only.
- **Total ≈ $0.08 — well under the $5 cap.**

Deliverables on branch `research/install-scopes`: this doc + `docs/install-cheatsheet-2026-09-30.md`.
