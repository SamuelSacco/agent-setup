# Install cheat sheet — copy-paste commands for Samuel

Date: 2026-09-30 ET. Every command below was re-executed live this session in a fake HOME and verified to succeed — this sheet contains no doc-only commands. Versions actually used: claude 2.1.286, copilot 1.0.89, skills CLI 1.7.0. Spend on this sheet: $0 (no model calls; success observable in files/list output).

Model defaults encoded (from `docs/install-scopes-2026-09-30.md`): skills → global; plugins → user scope (Claude default); MCP → user scope in Claude, project `.mcp.json` for team-shared; Copilot MCP → user only (workspace MCP is REFUTED on 1.0.89).

Each op: command, what it does, the flags that matter, how to confirm success, and one pitfall. Full mechanics + scope matrix in `docs/install-scopes-2026-09-30.md`.

---
## 1. Add a skill globally

```bash
npx -y skills add dbos-inc/agent-skills -g -y --agent claude-code github-copilot
```

One line: installs every skill in the repo to the global (user) scope,
targeting only the two agents you actually use.

Flags that matter: `-g` = global (default would be project + an interactive
scope prompt); `-y` = skip all confirmation prompts (mandatory under
automation — without it the run stops at the scope prompt and installs
nothing); `--agent claude-code github-copilot` = skip the 79-agent fan-out;
`-s/--skill <name>` = install only one skill from the repo.

Success check: real files land in the canonical store
`~/.agents/skills/<name>/` (e.g. `dbos-python`, `dbos-java`,
`dbos-typescript`); Claude sees them via symlinks
`~/.claude/skills/<name> -> ../../.agents/skills/<name>`; lock written to
`~/.agents/.skill-lock.json`. Copilot reads the canonical store directly
(`personal-agents` source) — no `~/.copilot/skills` is created.

> ⚠️ DON'T: run `-g -y` without `--agent` — it symlinks into ~56 agent
> dirs for agents you don't have installed. Also note this run's exit code
> was 2 even though the install succeeded — gate automation on the file
> check, not the exit code.

## 2. Add a skill to one project only

```bash
cd <project> && npx -y skills add dbos-inc/agent-skills -y --agent claude-code github-copilot --skill dbos-python
```

One line: installs one skill scoped to the current project directory.

Flags that matter: no `-g` = project scope; `-y` again mandatory
(defaults the scope prompt to Project and skips it); `--skill` picks the
skill.

Success check: real copy at `<project>/.agents/skills/dbos-python/`;
Claude symlink at `<project>/.claude/skills/dbos-python`; project lock at
`<project>/skills-lock.json` (the skill's `computedHash` is recorded there).
Nothing leaks to sibling projects.

> ⚠️ DON'T: put the same skill NAME in both global and project scope —
> Claude resolves the collision by **global wins** (PROVEN, W1 §6), so the
> project copy is silently ignored. A name must exist in exactly one scope.

## 3. List installed skills (global + project)

```bash
npx -y skills list -g --json        # global: path, source, sourceUrl per skill
cd <project> && npx -y skills list --json   # project: "scope": "project" entries
```

One line: the CLI's own inventory; `--json` gives machine-readable output.

Flags that matter: `-g` flips between global and project lists
(default without `-g` is project); `-a/--agent` can filter by agent.

Success check: each entry shows `name`, `path` (must start with
`~/.agents/skills/` for global, `<project>/.agents/skills/` for project),
and `scope`. Cross-check against the lock files (`~/.agents/.skill-lock.json`,
`skills-lock.json`) for drift.

> ⚠️ DON'T: rely on the human-readable list for audits — descriptions are
> cosmetic; compare `path` + lock `computedHash` instead.

## 4. Remove a skill (global / project)

```bash
cd <project> && npx -y skills remove dbos-python -y     # project
npx -y skills remove dbos-golang -g -y                  # global
```

One line: deletes the skill body, its agent symlinks, and rewrites the lock.

Flags that matter: `-g` for the global store (project is the default when
run in a project dir); `-y` skips confirmation; `--all` removes everything.

Success check: project — `dbos-python` gone from
`<project>/.agents/skills/` and `<project>/.claude/skills/`,
`skills-lock.json` shows `"skills": {}`. Global — gone from
`~/.agents/skills/`, `~/.claude/skills/`, and the `.skill-lock.json` entry.

> ⚠️ DON'T: delete the directories by hand — the lock file keeps a stale
> entry and symlinks dangle. Use `skills remove` so the lock is rewritten.

## 5. Install a Claude plugin at user scope (via marketplace)

```bash
claude plugin marketplace add anthropics/claude-plugins-official \
  --sparse .claude-plugin plugins/commit-commands
claude plugin install commit-commands@claude-plugins-official --scope user
```

One line: registers the marketplace once, then installs the plugin to user
scope (visible in every project).

Flags that matter: `--sparse <paths>` limits the git clone (full official
catalog is huge); `--scope user` is the default — say it anyway;
install takes `<plugin>@<marketplace>`.

Success check: `~/.claude/settings.json` gets BOTH
`extraKnownMarketplaces.<name>` (the marketplace declaration) AND
`enabledPlugins: {"commit-commands@claude-plugins-official": true}`;
payload lands in `~/.claude/plugins/cache/<marketplace>/<plugin>/<version-or-sha>/`
(this run: `.../hookify/aa5654b7acb7/`); `claude plugin list --json` shows
`scope: user, enabled: true`.

> ⚠️ DON'T: re-add the same marketplace name with a different `--sparse`
> set — a marketplace name has ONE source definition across scopes and the
> second add fails. Register it once with the full sparse set you'll ever
> need (`marketplace remove` + re-add is the fix). DON'T probe plugin
> visibility with `--bare` — bare mode skips plugin sync and reports the
> plugins as absent even when installed.

## 6. Install a Claude plugin project-scoped

```bash
cd <project> && claude plugin install hookify@claude-plugins-official --scope project
```

One line: installs the plugin so it loads only inside this project.

Flags that matter: `--scope project` (also `--scope local`, which writes
to `.claude/settings.local.json` instead).

Success check: enablement lands in `<project>/.claude/settings.json`
(`enabledPlugins`), NOT in `~/.claude/settings.json`. Registry
(`~/.claude/plugins/installed_plugins.json`) records `scope: project` with
the project path. From a sibling project, `plugin list --json` shows it as
`enabled: false` — enablement resolves per-cwd.

> ⚠️ DON'T: assume project plugins leak — they don't (verified from a
> sibling cwd). DON'T put a genuinely machine-personal plugin at project
> scope: project entries travel with the repo and prompt review by anyone
> who clones it.

## 7. List / enable / disable / uninstall a plugin

```bash
claude plugin list --json
claude plugin disable commit-commands@claude-plugins-official --scope user
claude plugin enable  commit-commands@claude-plugins-official --scope user
cd <project> && claude plugin uninstall hookify@claude-plugins-official --scope project
```

One line: list inventories; enable/disable flips one boolean; uninstall
removes the settings entry and registry record.

Success check: disable writes `"commit-commands@claude-plugins-official": false`
in that scope's settings file (payload stays on disk — a fresh headless
session immediately drops its skills); enable flips it back to `true`.
Uninstall removes the `enabledPlugins` entry and leaves the settings file as
`{"enabledPlugins": {}}`; the cache payload directory is orphaned (swept
later; `~/.claude/plugins/cache/...` may linger).

> ⚠️ DON'T: disable without `--scope` from inside a project — disable
> auto-detects scope and you may flip the wrong entry. And DON'T remove a
> marketplace to "clean up" unless you mean it: `plugin marketplace remove`
> **cascades** and uninstalls every plugin from that marketplace (PROVEN,
> including their saved data).

## 8. Add an MCP server at user scope (Claude)

```bash
claude mcp add -s user my-server -- python3 /path/to/server.py arg1
```

One line: registers a stdio MCP server in the user's global config,
connected in every project immediately.

Flags that matter: `-s user` is MANDATORY — the default scope is `local`
(silently per-project); the server NAME goes BEFORE `-e` (`-e` is variadic
and will swallow the name if it comes first); `--` separates the server
command from the CLI's flags.

Success check: entry appears at top-level `mcpServers.my-server` in
`~/.claude.json`; `claude mcp list` (from any project) shows
`my-server: ... - ✔ Connected`. `claude mcp get my-server` prints
`Scope: User config (available in all your projects)`.

> ⚠️ DON'T: pass secrets with `-e KEY=value` and then commit anything that
> echoes them — they land PLAINTEXT in `~/.claude.json` (file is
> `-rw-------`, but it's still plaintext). Prefer `claude mcp login` (OAuth)
> or inject at install time from a per-machine secrets file.

## 9. Add an MCP server project-scoped (Claude)

```bash
cd <project> && claude mcp add -s project my-server -- python3 /path/to/server.py arg1
```

One line: writes the server definition into the project's `.mcp.json` so
it travels with the repo.

Success check: `<project>/.mcp.json` is created with
`mcpServers.my-server`; NOTHING is written to `~/.claude.json`.
BUT: `claude mcp list` shows it as `⏸ Pending approval (run \`claude\` to
approve)` — project servers are approval-gated by design. Setting
`enabledMcpjsonServers` alone does NOT clear it; only the interactive trust
prompt (`hasTrustDialogAccepted: true` in `~/.claude.json`) connects it.
Subdirectories of the project see the same server.

> ⚠️ DON'T: expect headless `-p` sessions to use a fresh project server —
> they can't clear the approval gate. Budget one interactive `claude`
> session per machine per project. DON'T share a `.mcp.json` between Claude
> and Copilot formats — Claude rejects Copilot's `"type": "local"` entry
> with a config-diagnostics warning.

## 10. Add an MCP server at user scope (Copilot)

```bash
copilot mcp add my-server -- python3 /path/to/server.py arg1
```

One line: adds a server to Copilot's user config — the only scope that
loads on 1.0.89.

Flags that matter: there is NO scope flag — `add` is user-only by design;
`--env KEY=VALUE` repeatable; `--tools` (default `*`); `--timeout`;
`--json` for scripting; `--show-secrets` to print stored env values.

Success check: block appended to `~/.copilot/mcp-config.json` under top
key `mcpServers` with `"type": "local"` (Copilot's spelling — NOT `stdio`),
`"command"`, `"args"`, `"tools": ["*"]`; `copilot mcp list` shows the
server grouped under `user`, annotated `enabled: true`. A live session from
any project returns the server's pong.

> ⚠️ DON'T: waste time on Copilot workspace MCP (`.mcp.json`,
> `.github/mcp.json`, `.vscode/mcp.json`) — REFUTED on 1.0.89 across every
> documented location/key/type variant; nothing loads. User scope is the
> only delivery path today. Env values are stored PLAINTEXT; `mcp get`
> masks them (`***`) unless you pass `--show-secrets`.

## 11. Remove an MCP server per scope

```bash
claude mcp remove -s user my-server        # Claude user scope
cd <project> && claude mcp remove -s project my-server   # Claude project scope
copilot mcp remove my-server               # Copilot user config
```

One line: removes the server block from the scope's config file.

Success check: Claude — `Removed MCP server "my-server" from user|project
config`; entry gone from `~/.claude.json` (`mcpServers` empty `{}`) or
`<project>/.mcp.json` (`mcpServers: {}`). `claude mcp remove` with NO `-s`
auto-detects which scope holds the name (verified: removed a user server
from an unrelated cwd). Copilot — `Removed server "my-server"`; block gone
from `~/.copilot/mcp-config.json` (workspace servers can only be removed by
editing their config files — `copilot mcp remove` refuses them).

> ⚠️ DON'T: rely on `remove` without `-s` when the same name exists in two
> Claude scopes — keep names unique per scope so the auto-detect has no
> ambiguity. For rotation, re-add with the new value; there is no
> edit-in-place.

## 12. Check/update drift: what's installed, what's stale

```bash
# Plugins (Claude) — re-run the marketplace refresh + per-plugin check:
claude plugin marketplace update claude-plugins-official
claude plugin update commit-commands@claude-plugins-official --scope user --json
# → {"updateOutcome":"up_to_date","oldVersion":"aa5654b7acb7",...}
#    or "updated" with old/new SHAs. Cache dirs are keyed by git SHA, so
#    a SHA change IS the drift signal.

# Skills — re-contact GitHub and re-hash:
npx -y skills update -g -y            # global
npx -y skills update -y               # project (auto: project if in one)

# Drift audit triad (compare against the canonical record / pin file):
npx -y skills list -g --json           # names + paths; diff lock computedHash vs pins
claude mcp list                       # ✔ Connected vs ⏸ Pending approval vs vanished
copilot mcp list                      # source: user + enabled flags per server
```

One line: `plugin update`/`marketplace update`/`skills update` refresh from
upstream; the three `list` commands are the audit baseline.

Success check: `updateOutcome: up_to_date` (or a recorded SHA bump);
`skills update` reports `✓ All global skills are up to date`. The model rule:
never `skills update -g -y` on a live home without re-pinning — the update
moves every project at once and the pin file will fail `verify` loudly,
which is the intended alarm.

> ⚠️ DON'T: run `skills update -g -y` as a casual refresh — it's a 79-agent
> fan-out with no version pin update. Treat updates as deliberate, recorded
> actions (edit canonical → review → re-pin → replay), not background
> refreshes.

---

## NOT-VERIFIED appendix

None — all 12 operations re-executed to success this session. (Design-only item, not one of the ops: the weekly `verify` cron, name-collision lint, and secrets scan from the judged model are designed, not built.)
