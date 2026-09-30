# P2 Install-Surface Matrix — 2026-09-30

Workstream W1. Tools: Claude Code 2.1.285 (`~/workspace/tools/bin/claude`), Copilot CLI 1.0.89
(`~/workspace/tools/bin/copilot`), both on `claude-haiku-4-5-20251001` via the stored Anthropic key
(Claude: apiKeyHelper; Copilot: BYOK env). All runs isolated: `HOME=<case>/home`, cwd `<case>/proj`,
scratch under `~/workspace/p2/w1/scratch/<case>/`. Every verdict rests on disk state (marker files,
config files, session-event logs), never on agent self-report.

Probe fixtures (committed): `evals/fixtures/w1-install-probes/` — marker skill `a-probe`/`b-probe`
(write `<x>-skill-invoked.txt` containing a token), plugin source `plugsrc` (skill `p-probe`, agent
`p-agent`, `hooks/hooks.json`, `.mcp.json`), minimal stdio MCP server `mcp_server.py` (one tool
`w1_ping` → `W1MCPMARKER`; verified standalone over JSON-RPC before any CLI run).

## Matrix

Verdicts: PROVEN = invoked by name in a headless run, effect verified on disk. REFUTED = path does
not exist / did not fire, with evidence. UNVERIFIABLE = not tested.

| Capability | Path | Claude Code | Copilot CLI |
|---|---|---|---|
| Skill | (a) `npx skills add` | **PROVEN** project + global | **PROVEN** project + global |
| Skill | (b) in-tool | **PROVEN** via plugin install and via `claude plugin init` (skills-dir); no standalone skill-install command exists | **PROVEN** via `copilot skill add` and via plugin install |
| Skill | (c) `scripts/install.sh` | **PROVEN** | **PROVEN** |
| Agent | (a) `npx skills add` | **REFUTED** — no agent concept in the CLI | **REFUTED** — same |
| Agent | (b) in-tool | **PROVEN** via plugin bundle only; no standalone agent-install command exists | **PROVEN** via plugin bundle only; no standalone agent-install command exists |
| Agent | (c) `scripts/install.sh` | **PROVEN** | **PROVEN** |
| Plugin | (a) `npx skills add` | **REFUTED** — skills only, no plugin concept | **REFUTED** — same |
| Plugin | (b) in-tool | **PROVEN** marketplace add + install (local marketplace); remote marketplace source **UNVERIFIABLE** (not tested) | **PROVEN** local-path install and marketplace install (`spark@copilot-plugins`, incl. invocation of its bundled skill) |
| Plugin | (c) `scripts/install.sh` | **REFUTED** — repo has no `canonical/plugins/`; `install.sh`/`adapters.py` handle skills/agents/mcp/hooks only | **REFUTED** — same |
| Hook | (a) `npx skills add` | **REFUTED** — no hook concept in the CLI | **REFUTED** — same |
| Hook | (b) in-tool | **PROVEN** via plugin `hooks/hooks.json` (`PostToolUse` fired, marker log written); no standalone hook-install command in either tool | **PROVEN** via plugin `hooks/hooks.json` (same Claude-shaped file fired, marker log written) |
| Hook | (c) `scripts/install.sh` | **PROVEN** — `PostToolUseFailure` → sidecar event appended on induced failure | **REFUTED** for shell-failure capture — `postToolUseFailure` did not fire on a failing shell command; sidecar unchanged (mechanism: E4 addendum — the shell tool reports success at tool layer; capture would need a `postToolUse` payload-parsing hook, not built) |
| MCP server | (a) `npx skills add` | **REFUTED** — no MCP concept in the CLI | **REFUTED** — same |
| MCP server | (b) in-tool | **PROVEN** via `claude mcp add` (standalone) and via plugin `.mcp.json` | **PROVEN** via `copilot mcp add` (standalone) and via plugin `.mcp.json` |
| MCP server | (c) `scripts/install.sh` | **PROVEN** — root `.mcp.json` | **PROVEN by invocation, adapter defect** — see §C-MCP: discovery rides on the root `.mcp.json`; the adapter's own `.github/mcp.json` is malformed for Copilot and skipped |

## Path (a) — `npx skills add` (package `skills`, via `npx -y skills`)

Facts:
- Local directory source is supported: `npx -y skills add <abs path to skillpkg> --list -y` →
  "Local path validated / Found 1 skill". GitHub shorthand and URLs are the documented sources
  (`skills --help`).
- Project install command used: `npx -y skills add <skillpkg> --all` (`--all` = `--skill '*' --agent '*' -y`).
  Output: "Installing to all 79 agents"; most skipped ("project directory not found").
- Files written, project scope (case `a1`):
  - Canonical copy (real file): `proj/.agents/skills/a-probe/SKILL.md`
  - Symlink: `proj/.claude/skills/a-probe -> ../../.agents/skills/a-probe` (`ls -la` verified)
  - Copy for one further agent: `proj/agent/skills/a-probe/SKILL.md`
  - Lockfile: `proj/skills-lock.json` (`sourceType: "local"`, `computedHash`)
  - Nothing written for Copilot: no `.github/`, no `~/.copilot/` entry. Copilot reads
    `.agents/skills/` directly (its `skill --help` lists project sources `.github/skills/`,
    `.agents/skills/`, `.claude/skills/`; personal sources `~/.copilot/skills/`, `~/.agents/skills/`).
- Global install command: `npx -y skills add <skillpkg> -g --agent claude-code github-copilot -y`.
  Files: canonical copy `home/.agents/skills/a-probe/SKILL.md`; symlink
  `home/.claude/skills/a-probe -> ../../.agents/skills/a-probe`. Again no Copilot-specific file.
- Invocation evidence:
  - Claude, project: result `W1A_SKILL_MARKER`, `proj/a-skill-invoked.txt` on disk with the token.
  - Copilot, project: `a-skill-invoked.txt` on disk; session events contain `skill.invoked` and the
    reasoning records the skill body text.
  - Claude, global (empty project): result `W1A_SKILL_MARKER`, marker file written.
  - Copilot, global: marker file written; `skill.invoked` event with
    `path: <home>/.agents/skills/a-probe/SKILL.md`.
- `--copy` flag exists (copy instead of symlink) — not tested, UNVERIFIABLE.
- Non-skill capabilities: `skills --help` lists only skill commands (`add/use/remove/list/find/
  update/init/experimental_install/experimental_sync`). No agent, hook, MCP, or plugin command.

## Path (b) — in-tool installation

### Claude Code

Subcommand inventory (`claude --help`): `mcp`, `plugin|plugins`, plus `agents` (background-session
manager, not an agent installer). No skill/agent/hook install subcommand outside `plugin`.

Plugin, local marketplace (case `bclaude`):
- Commands: `claude plugin marketplace add <abs path to market dir>` →
  "Successfully added marketplace: w1-market (declared in user settings)";
  `claude plugin install w1-plugin@w1-market -y` → installed, scope: user.
- Files written:
  - Payload copy: `home/.claude/plugins/cache/w1-market/w1-plugin/0.1.0/` (full plugin tree)
  - `home/.claude/plugins/installed_plugins.json` (installPath, version, timestamps)
  - `home/.claude/plugins/known_marketplaces.json`
  - `home/.claude/settings.json`: `enabledPlugins: {"w1-plugin@w1-market": true}`,
    `extraKnownMarketplaces.w1-market.source = {source: "directory", path: <market dir>}`
- `claude plugin details w1-plugin@w1-market` inventory: Skills (1) p-probe; Agents (2) p-agent,
  p-agent.agent; Hooks (1) PostToolUse; MCP servers (1) w1mcp; ~64 always-on tokens.
- One combined probe run (steps: invoke plugin skill, delegate to plugin agent, call plugin MCP
  tool, run bash):
  - Skill: `p-skill-invoked.txt` = `W1P_SKILL_MARKER` on disk. PROVEN.
  - Agent: `p-agent-invoked.txt` = `W1P_AGENT_MARKER` on disk. PROVEN.
  - Hook: `plugin-hook.log` received 3 `fired` lines from the plugin's `PostToolUse` hook. PROVEN.
  - MCP: first attempt blocked on permissions — the plugin MCP tool is namespaced
    `mcp__plugin_w1-plugin_w1mcp__w1_ping`; an allowlist entry for `mcp__w1mcp` does not cover it.
    Re-run with the namespaced tool allowed: result exactly `W1MCPMARKER`. PROVEN.
- Plugin manifest that worked for both tools: `.claude-plugin/plugin.json` (`{"name","version",
  "description"}`), components at plugin root: `skills/<n>/SKILL.md`, `agents/*.md`,
  `hooks/hooks.json`, `.mcp.json`.

`claude plugin init` (case `btool`):
- `claude plugin init w1-scaffold` → creates `home/.claude/skills/w1-scaffold/` containing
  `.claude-plugin/plugin.json` and `SKILL.md` (template body); message: "It will auto-load next
  session as w1-scaffold@skills-dir."
- Probe: Claude invoked `w1-scaffold` by name and quoted its heading/TODO body verbatim. PROVEN
  (scaffold is a skills-dir plugin, user scope, no marketplace involved).

`claude mcp add` (case `btool`):
- `claude mcp add w1mcp -- python3 <abs path to mcp_server.py>` (default scope: local) →
  writes into `home/.claude.json` under the project key (not into `proj/.mcp.json`);
  `claude mcp list` health check: `w1mcp … ✔ Connected`.
- Probe with `mcp__w1mcp__w1_ping` allowed: result exactly `W1MCPMARKER`. PROVEN.

### Copilot CLI

Subcommand inventory (`copilot --help`): `plugin`, `mcp`, `skill`, `instruction`, `lsp`, others.
No agent or hook install subcommand; agents/hooks arrive only via plugins or hand-placed files.

`copilot skill add` (case `bcopin`):
- `copilot skill add <abs path to SKILL.md>` → "Added personal skill "b-probe" from file.
  Created /…/home/.copilot/skills/b-probe" — a copy at `home/.copilot/skills/b-probe/SKILL.md`.
  `copilot skill list` shows it under "Personal skills". (`--project` variant writes to
  `.github/skills/` per `--help`; not separately probed.)
- Probe: `skill.invoked` event (`name: b-probe`, `source: "personal-copilot"`), marker file
  `b-skill-invoked.txt` on disk. PROVEN.

`copilot mcp add` (case `bcopin`):
- First attempt REFUSED: "Failed to write configuration to …/home/.copilot/mcp-config.json: The
  storage directory is writable by group or other users. Choose a private COPILOT_HOME, or review
  write permissions on a directory you own". (Scratch homes inherit the workspace's group-writable
  setgid perms.) After `chmod 700` on the home and `.copilot` dirs, the same command succeeds.
- Writes `home/.copilot/mcp-config.json`:
  `{"mcpServers": {"w1mcp": {"tools": ["*"], "type": "local", "command": "python3", "args": [<abs path>]}}}`
- Probe (same run as the skill probe): tool `w1mcp-w1_ping` executed (session events), marker
  `W1MCPMARKER` in the session log (3 occurrences; the prompt never contained the token). PROVEN.

Plugin, local path (case `bcopplug`):
- `copilot plugin install <abs path to plugsrc copy>` → `Plugin "w1-plugin" installed successfully.
  Installed 1 skill.` plus verbatim warning: "Direct plugin installs (repos, URLs, local paths) are
  deprecated. Only plugin@marketplace installs will be supported in a future release."
- Payload copy: `home/.copilot/installed-plugins/_direct/plugsrc/` (whole tree). Also
  `home/.copilot/installed-plugins.lock`, `config.json`, `settings.json`.
- Installer summary under-reports: it printed "Installed 1 skill", but `copilot skill list` shows
  `p-probe` under "Plugin skills" and `copilot mcp list` shows `w1mcp` under "Plugin servers", and
  the combined probe then proved all four surfaces:
  - Skill: `skill.invoked` (p-probe) + `p-skill-invoked.txt` on disk. PROVEN.
  - Agent: `p-agent-invoked.txt` = `W1P_AGENT_MARKER` on disk (delegation via the `task` tool).
    PROVEN.
  - MCP: tool `w1mcp-w1_ping` executed; `W1MCPMARKER` in events. PROVEN.
  - Hook: `plugin-hook.log` received 3 `fired` lines; the file that fired is the Claude-shaped
    `hooks/hooks.json` (`hooks.PostToolUse[].hooks[].command`). PROVEN.
- Plugin source for this case additionally carried `plugin.json` at the root (duplicate of
  `.claude-plugin/plugin.json`) and both `mcpServers` and `servers` keys in `.mcp.json`; which of
  the duplicate manifests Copilot read was not isolated.

Plugin, marketplace (case `bcopmkt`):
- Default marketplaces present without any registration or GitHub auth: `copilot-plugins`
  (github/copilot-plugins), `awesome-copilot` (github/awesome-copilot). `marketplace browse
  copilot-plugins` lists plugins.
- `copilot plugin install spark@copilot-plugins` → installed; payload at
  `home/.copilot/installed-plugins/copilot-plugins/spark/` (`README.md`,
  `skills/spark-app-template/SKILL.md` + references).
- Probe: `skill.invoked` event (`name: spark-app-template`, `pluginName: "spark"`). PROVEN.

## Path (c) — canonical `scripts/install.sh`

Setup (case `c1`): scratch copy of the repo; three probe definitions added to the copy's
`canonical/` only (skill `w1c-probe`, agent `w1c-agent`, MCP server `w1ping` → the fixture
`mcp_server.py`); `.claude/settings.json` pre-seeded with `apiKeyHelper`; `./scripts/install.sh` run
in the copy. Adapter output (unchanged from the repo's `scripts/adapters.py`):

- Skills → `.claude/skills/<n>/SKILL.md` and `.github/skills/<n>/SKILL.md` (copies)
- Agents → `.claude/agents/<n>.md` and `.github/agents/<n>.agent.md`
- MCP → root `.mcp.json` (`{"mcpServers": …}`) and `.github/mcp.json` (`{"servers": …}`)
- Hooks → `.claude/settings.json` `hooks.PostToolUseFailure` → `./scripts/sidecar.sh record-failure`
  (adapter preserved the pre-existing `apiKeyHelper` key); `.github/hooks/failure-capture.json`
  (`version: 1`, `postToolUseFailure`, `bash` field)

Claude combined probe (invoke `w1c-probe`, delegate to `w1c-agent`, call `w1_ping` from `w1ping`,
run `python --version`):
- `c-skill-invoked.txt` = `W1C_SKILL_MARKER`; `c-agent-invoked.txt` = `W1C_AGENT_MARKER`;
  MCP result `W1MCPMARKER`; the bash command exited 127 and `wiki/telemetry/events.jsonl` grew
  1 → 2 lines, the new line a parseable `tool_failure` event with `hook_event_name:
  "PostToolUseFailure"`, `tool_name: "Bash"`. All four PROVEN in one run.

Copilot combined probe (same prompt, markers deleted first, `COPILOT_ALLOW_ALL=true`):
- Skill: `skill.invoked` (w1c-probe) + `c-skill-invoked.txt` on disk. PROVEN.
- Agent: `c-agent-invoked.txt` = `W1C_AGENT_MARKER` on disk (delegation via `task` tool). PROVEN.
  (Contrast E6 pilot, where a Copilot agent run claimed success and wrote nothing; here the file
  is on disk.)
- MCP: tool `w1ping-w1_ping` executed, `W1MCPMARKER` in events. PROVEN — but see §C-MCP.
- Hook: `python --version` failed (127); `wiki/telemetry/events.jsonl` unchanged (stayed 2 lines).
  REFUTED for shell-failure capture on v1.0.89.

### §C-MCP — adapter defect, isolated without any model run

- In the installed copy's project dir, `copilot mcp list` printed "No MCP servers configured"
  without `COPILOT_ALLOW_ALL`, and listed both workspace servers with it: workspace MCP config is
  trust-gated by the same directory-trust switch.
- Isolation tests in empty dirs with `COPILOT_ALLOW_ALL=true`:
  - Only root `.mcp.json` (`mcpServers` key) present → both servers listed.
  - Only `.github/mcp.json` with the adapter's `{"servers": …}` → warning: `skipping workspace MCP
    config ".github/mcp.json" because it is malformed: mcpServers: Required`; no servers listed.
  - Only `.github/mcp.json` rewritten with `{"mcpServers": …}` → both servers listed.
- Conclusion: Copilot requires the `mcpServers` key in workspace MCP files. The adapter's
  `.github/mcp.json` (`servers` key) is dead output; Copilot's canonical-path MCP discovery works
  only because the root `.mcp.json` (written for Claude) is also read by Copilot.

## Cost log

Budget cap $3.00. Total spent: **$0.65**. Claude costs are `total_cost_usd` from `--output-format
json`. Copilot costs are token counts from session-state `events.jsonl` converted at Haiku rates
($1/M input, $5/M output; input count is the session total record, main + subagent where a summed
record exists). Two early Claude invocations failed pre-flight on a wrong cwd at $0.00 and are
counted below.

| # | Run | Cost |
|---|---|---|
| 1 | (a) Claude, a-probe, project | $0.0355 (4 turns) |
| 2 | (a) Claude, 2 failed runs (wrong cwd, "Not logged in", 0 tokens) | $0.0000 |
| 3 | (a) Copilot, a-probe, project — 48,172 in / 430 out | $0.0503 |
| 4 | (a) Claude, a-probe, global | $0.0187 |
| 5 | (a) Copilot, a-probe, global — 48,204 in / 412 out | $0.0503 |
| 6 | (b) Claude plugin combined probe (skill+agent+hook+MCP attempt) | $0.0592 (8 turns) |
| 7 | (b) Claude plugin MCP re-probe (namespaced tool allowed) | $0.0174 |
| 8 | (b) Claude `mcp add` probe | $0.0172 |
| 9 | (b) Claude `plugin init` scaffold invocation | $0.0151 |
| 10 | (b) Copilot `skill add` + `mcp add` combined probe — 48,586 in / 477 out | $0.0510 |
| 11 | (b) Copilot plugin (local) combined probe — 73,232 in / 1,159 out | $0.0790 |
| 12 | (b) Copilot marketplace `spark` skill probe — 37,033 in / 432 out | $0.0392 |
| 13 | (c) Claude combined probe | $0.0792 (8 turns) |
| 14 | (c) Copilot combined probe — 132,218 in / 1,237 out | $0.1384 |
| | **Total** | **$0.6505** |

Non-model operations (installs, `--help`, `list`, `details`, marketplace browse, isolation tests)
cost $0 and are cited inline above.

## Factual notes per path

(a) `npx skills add`:
- One command fans a skill out to many agents from a single canonical copy in `.agents/skills/`;
  per-agent entries are symlinks by default. It installs skills and nothing else.
- Copilot needs no Copilot-specific output from it: it reads `.agents/skills/` (project and
  personal) natively.
- A lockfile (`skills-lock.json`) records source + hash per skill.

(b) In-tool:
- Claude: one mechanism (`plugin`) covers skills, agents, hooks, MCP as a bundle; standalone
  commands exist only for MCP (`claude mcp add`) and for scaffolding a new plugin
  (`claude plugin init`). Plugin install is user-scope by default and copies the payload into
  `~/.claude/plugins/cache/`.
- Copilot: three mechanisms — `copilot skill add` (skills, copy into `~/.copilot/skills/`),
  `copilot mcp add` (MCP, user config file; refuses group/other-writable config dirs), and
  `copilot plugin install` (bundles; marketplace form is the supported one, direct/local installs
  print a deprecation warning).
- The same plugin source tree (`.claude-plugin/plugin.json` + root-level `skills/`, `agents/`,
  `hooks/hooks.json`, `.mcp.json`) installed and fired under both tools, including the
  Claude-shaped hook file under Copilot.
- Plugin MCP tools are namespaced under Claude (`mcp__plugin_<plugin>_<server>__<tool>`);
  permission allowlists must use the namespaced name.

(c) Canonical `install.sh`:
- One run materializes both tools' layouts from `canonical/`; the Claude half is fully proven
  (skill, agent, MCP, failure hook in a single run).
- Copilot half: skill and agent proven by invocation; MCP proven by invocation but through the
  root `.mcp.json`, with the adapter's `.github/mcp.json` malformed for Copilot (§C-MCP — adapter
  fix: emit `mcpServers`, not `servers`); failure hook refuted for shell failures.
- Copilot workspace-level config (MCP, hooks) is invisible until the directory is trusted
  (`COPILOT_ALLOW_ALL=true`); `copilot mcp list` without it reports an empty config even when the
  files are present and correct.
- No plugin path exists in the canonical system: there is no `canonical/plugins/` and the adapter
  emits no plugin bundle.

## Method caveats

- Scratch cases nest inside this repo, so Claude also saw the parent repo's root `.mcp.json` /
  `.claude/settings.json` while running in a case (observed: `filesystem-wiki` "Pending approval"
  in case `btool`'s `claude mcp list`). All verdicts rest on case-specific marker tokens, marker
  files, and session events, not on file presence, so the leak does not support any cell.
- Copilot token totals include cache-read/write tokens inside the reported input count; the
  conversion is the brief's flat Haiku-rate formula, not a billed-amount claim.
- Claude remote (GitHub) marketplace add/install was not tested; the local-directory marketplace
  path was. Copilot's marketplace path was tested against the bundled public marketplace.
