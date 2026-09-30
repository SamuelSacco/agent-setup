# Copilot CLI surface deep-dive — Phase 2

Date: 2026-09-30. Target: GitHub Copilot CLI **v1.0.89** (installed binary
`~/workspace/tools/bin/copilot`; bundle `~/.cache/copilot/pkg/linux-x64/1.0.89/`).
Sources: binary `--help` / `help <topic>` output, bundle inspection
(`app.js`, `definitions/`, `builtin-skills/`), official GitHub docs,
and this repo's live evals (E1/E2/E4). Verdicts: **PROVEN** /
**REFUTED** / **UNVERIFIABLE**, source named per claim. Companion to
`2026-09-30-copilot-cli-docs.md` (docs-only pass); this file adds the
binary/help axis and the plugin + built-in-agent inventory that pass lacked.

Config home: `~/.copilot/` (`COPILOT_HOME` overrides). Observed contents:
`config.json`, `settings.json`, `mcp-config.json`, `providers.json`,
`installed-plugins/` + `installed-plugins.lock`, `session-state/`, `logs/`.

## 1. Plugins — PROVEN (help + docs)

A full plugin system exists, managed by `copilot plugin` and the
in-session `/plugin` commands: `install | uninstall | update | list |
enable | disable | marketplace <add|remove|list|browse|update>`.

- **Sources:** `plugin@marketplace`, `owner/repo`, `owner/repo:path`,
  direct git URL, local path.
- **Marketplaces:** a git repo (any host, or local FS) containing a
  `marketplace.json` whose `plugins` array entries carry name,
  description, version, and path to the plugin directory. Two ship
  registered by default: `copilot-plugins` (github/copilot-plugins) and
  `awesome-copilot` (github/awesome-copilot). Docs list Anthropic's
  `claude-code-plugins` as an addable example — the marketplace mechanism
  is not GitHub-only.
- **Manifest:** `plugin.json` at the plugin root. Two formats:
  - *Agent Plugins 1.0* — manifest declares
    `$schema: https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`.
    Portable subset only: skills discovered from `skills/`, MCP config
    from `mcp.json` at root, fixed locations. Copilot-specific
    components (agents, hooks, commands, rules, LSP) live under
    `com.github.copilot/` and other clients ignore that directory.
  - *Legacy Copilot* — no `$schema`; configurable component paths;
    components at root: `agents/`, `skills/`, `hooks.json` (or `hooks/`),
    `.mcp.json` / `.github/mcp.json` / manifest `mcpServers` field,
    `lsp.json`.
- **Components a plugin can bundle:** custom agents (`*.agent.md`),
  skills (`skills/<name>/SKILL.md`), hooks, MCP server configs, LSP
  server configs.
- **Install state:** `~/.copilot/installed-plugins/` (+ lock file);
  empty on this machine (`copilot plugin list` → "No plugins installed").
- **Declarative install:** `enabledPlugins` field in user
  `~/.copilot/settings.json` or repo `.github/copilot/settings.json`;
  non-default marketplaces via `extraKnownMarketplaces` in the same
  files. Plugin-installed agents are hot-loaded; hand-placed files need
  a CLI restart (see §2).

**Claude Code equivalent:** yes — `/plugin`, `marketplace.json`,
`.claude-plugin/plugin.json`. Near-isomorphic design.
**Adapter verdict:** canonical→plugin is renderable. Agent Plugins 1.0
is the portable core (skills + MCP travel across clients by design);
agents/hooks/LSP are per-client payloads in both ecosystems, so one
canonical source renders two plugin layouts. Not tool-native only.

URLs: https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-cli-plugins ·
https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace

## 2. Custom agents — PROVEN (docs + bundle); one collision rule UNVERIFIABLE

- **Format:** `*.agent.md` = YAML frontmatter + Markdown prompt body.
  Frontmatter fields seen in docs and the bundle's wire format: `name`,
  `description` (required), `tools` (default: all), `model` (IDs or
  display names), `skills` (skills to eager-load at invocation),
  `mcpServers`, `userInvocable`, `disableModelInvocation`.
- **Locations:**
  - Project: `.github/agents/` — PROVEN (bundle string + docs). Project
    placement from the `/agent` create flow also offers `.claude/agents/`
    (crossover read) — docs/workshop sourced.
  - Personal: `~/.copilot/agents/` — PROVEN (docs config-dir reference,
    GitHub's own CLI course repo). Zero literal hits in `app.js`;
    resolution happens native-side, so binary-axis confirmation is
    UNVERIFIABLE.
  - Org/enterprise: `agents/` at the root of the org's `.github` or
    `.github-private` repository — PROVEN (docs).
- **Invocation:** `--agent <name>` flag, `/agent` picker in-session,
  natural-language request, or inference from the `description`.
  Hand-created/edited files require a CLI restart to load; plugin
  installs hot-load.
- **Name collision:** GitHub's own materials disagree. The CLI
  config-dir reference says project agents take precedence over
  personal; GitHub's CLI workshop says the `~/.copilot/agents/` copy
  wins. **UNVERIFIABLE** which v1.0.89 honors — setup rule: never ship
  the same agent name at two scopes.

### Built-in agents shipped in the bundle — PROVEN (`definitions/*.agent.yaml`)

| Agent | Function | Notes |
|---|---|---|
| `code-review` | Read-only review of staged/unstaged/branch diffs; high-confidence bugs, security, logic errors only | tools `*` |
| `explore` | Fast codebase Q&A in a separate context window; safe to call in parallel | model chain gpt-5.6-luna → gpt-5.4-mini, reasoning effort low |
| `rem-agent` | Memory consolidation: reads session trajectory, prunes/updates the context board | only tool is `context_board`; launched in background by `/subconscious`; "do not invoke spontaneously" |
| `research` | Autonomous research subagent: repo search, file fetch, claim verification, cited findings | model claude-sonnet-5 |
| `rubber-duck` | Cross-model critic for plans/designs/code; model selected dynamically at runtime (the cross-model property) | manual invocation by default; `rubberDuckAutoInvoke` opt-in (per tips research) |
| `security-review` | Security-only diff review across 11 vulnerability categories, false-positive-averse | tools `*` |
| `task` | Runs builds/tests/linters in a side context; brief summary on success, full output on failure | model chain gpt-5.6-luna → gpt-5.4-mini → claude-haiku-4.5 |

Plus `definitions/sidekick/` — internal, not a user surface:
`session-search`, `github-context`, `github-context-memory`,
`subconscious-agent` (+ test fixtures).

**Claude Code equivalent:** yes — `.claude/agents/*.md` project +
`~/.claude/agents/` user, same frontmatter+body shape.
**Adapter verdict:** renderable, near 1:1. Field sets differ (Copilot:
`skills`, `mcpServers`; Claude: its own extras), so the adapter renders
per-tool frontmatter from canonical fields. Bonus: Copilot reads
`.claude/agents/`, so a Claude placement can serve both — but relying on
the crossover makes Copilot behavior depend on a Claude-shaped dir;
explicit dual render stays the defensible default.

URLs: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli ·
https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference

## 3. Skills — PROVEN (help text, verbatim paths)

`copilot skill --help` enumerates discovery directly:

- **Project:** `.github/skills/`, `.agents/skills/`, `.claude/skills/`
- **Personal:** `~/.copilot/skills/`, `~/.agents/skills/`
- **Plugin:** skills bundled in installed plugins
- **Custom:** directories registered with `copilot skill add <directory>`
  (persisted in settings)

Management: `copilot skill list | add | remove | enable | disable`.
`skill add` takes a directory (registered), a local `SKILL.md`, or an
HTTPS URL; file/URL skills materialize to `~/.copilot/skills/<name>/SKILL.md`,
or the project's `.github/skills/` with `--project`. Name comes from
`SKILL.md` frontmatter. Format is the Agent Skills standard — the same
`SKILL.md` Claude Code consumes.

Built-in skills ship in the bundle (`builtin-skills/`):
`customize-cloud-agent`, `discover-resources`, `github-pr-media`.
Note: `copilot skill list` on this machine surfaces only the first and
third as available builtins; `discover-resources` exists on disk but is
not listed. Why: UNVERIFIABLE (gating suspected, not tested).

E1 already proved the operational claim: one canonical skill placed by
our installer is discovered and invoked by name in Copilot.

**Claude Code equivalent:** yes — `.claude/skills/` + `~/.claude/skills/`.
**Adapter verdict:** the strongest mapping of any surface. Copilot reads
`.claude/skills/` and `.agents/skills/` natively at project scope, so a
single canonical placement can serve both tools with zero translation;
our installer currently targets `.github/skills/` for Copilot, which is
equally native. Direct placement, no rendering.

URL: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills

## 4. MCP — PROVEN (help + docs)

- **Sources, lowest→highest precedence:** plugin-bundled < user
  `~/.copilot/mcp-config.json` < project files. Project files are found
  walking cwd → repo root; in the same directory `.mcp.json` beats
  `.github/mcp.json`; on name conflicts the file nearer the cwd wins;
  project definitions beat user config.
- **Format:** top-level `mcpServers` object (project files also accept a
  bare top-level server map). Server fields: `type` (`local`/stdio,
  `http`, `sse`), `command`/`args`/`env`, `url`/`headers`, `tools`
  filter (`*` default), timeout. The VS Code `.vscode/mcp.json` is
  **not** read — it uses the unsupported `servers` key (REFUTED as a
  Copilot source).
- **Built-in:** `github-mcp-server` (http) is always configured.
- **Trust gate:** project-level servers load only in trusted
  directories and are silently skipped otherwise; in prompt mode an
  untrusted dir needs `GITHUB_COPILOT_PROMPT_MODE_WORKSPACE_MCP=true`.
- **Management:** `copilot mcp list | get | add | remove | enable |
  disable` (`add` writes user config only), `/mcp` in-session, `/mcp
  search` against the MCP Registry (experimental).

**Claude Code equivalent:** yes — project `.mcp.json` (same filename,
same `mcpServers` key), user scope in `~/.claude.json`.
**Adapter verdict:** near-direct. One canonical MCP definition renders
to a shared project `.mcp.json` both tools read; user scope needs two
writes (`~/.copilot/mcp-config.json` vs `~/.claude.json`). Our installer
currently writes `.github/mcp.json` for Copilot — native and valid, but
`.mcp.json` at root is the one-file-two-tools option.

URL: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers

## 5. Hooks — PROVEN as a surface; failure event REFUTED for shell failures (E4)

- **Locations:** repo `.github/hooks/*.json`; user `~/.copilot/hooks/*.json`
  (`$COPILOT_HOME/hooks/`); inline `hooks` key in `~/.copilot/settings.json`
  and repo settings (bundle config docs: keyed by event name, same schema
  as `.github/hooks/*.json`); plugin `hooks.json`. Sources combine —
  policy, then user, then project, then plugins; every entry registered
  for an event runs.
- **Format:** JSON, `version: 1`, `hooks` object mapping event → array
  of `{ bash | powershell | command | exec, timeoutSec }` (default 30s).
  Loaded at CLI start; no hot reload.
- **Events (14 documented):** `sessionStart`, `sessionEnd`,
  `userPromptSubmitted`, `userPromptTransformed`, `preToolUse`,
  `postToolUse`, `postToolUseFailure`, `permissionRequest`,
  `errorOccurred`, `notification`, `preCompact`, `subagentStart`,
  `subagentStop`, `agentStop`. One format is shared with the Copilot
  cloud agent.
- **Trust model (the load-bearing fact):** repo hooks load only when
  the working directory is trusted. Untrusted headless runs fire
  nothing — E4's original 0/5. `COPILOT_ALLOW_ALL=true` (the exact
  string; other truthy spellings only auto-approve tools) additionally
  trusts the cwd, per `copilot help environment`, and then
  `sessionStart`/`preToolUse`/`postToolUse` fire (E4 retest, markers
  produced). `GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS=1` did **not**
  unlock repo hooks in the retest — REFUTED as an unlock mechanism.
- **Failure gap:** `postToolUseFailure` never fired for shell failures
  on v1.0.89, including exit 127 — the shell tool reports
  `resultType: "success"` and buries the exit code in
  `toolResult.textResultForLlm`. Copilot failure capture = `postToolUse`
  hook + parse the payload. Adapter identified, not built. Whether the
  event fires for non-shell tool classes: UNVERIFIABLE (untested).

**Claude Code equivalent:** yes, larger event set in `settings.json`,
and `PostToolUseFailure` does discriminate failures there (E4: Claude
5/5). No equivalent of Copilot's directory-trust gate on repo hooks.
**Adapter verdict:** renderable per-event, not 1:1. Canonical hook
intent renders to both formats, but failure capture needs a
Copilot-specific payload-parsing adapter; treat each event as its own
contract.

URLs: https://docs.github.com/en/copilot/concepts/agents/hooks ·
https://docs.github.com/en/copilot/reference/hooks-reference ·
evidence: `evals/results/2026-09-30-E4.md` (addendum)

## 6. Instructions — PROVEN; precedence is surface-dependent (docs disagree)

`copilot instruction list` exists precisely because this surface is
multi-source; run in this repo it reports `AGENTS.md` and `CLAUDE.md`
as the discovered repository instructions.

- **User scope:** `$COPILOT_HOME/muse-instructions.md`,
  `$COPILOT_HOME/instructions/**/*.instructions.md`.
- **Repo scope:** `.github/muse-instructions.md`,
  `.github/instructions/**/*.instructions.md` (path-scoped via `applyTo`
  frontmatter globs), plus `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`,
  `GEMINI.md`, `.claude/rules/**/*.md`, and any dirs in
  `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`.
- **Discovery:** repo root, cwd, intermediate directories, and
  directories of files being worked on; for nested `AGENTS.md`, nearest
  wins. `@relative/path` imports expand inside
  `muse-instructions.md` / `AGENTS.md` / `CLAUDE.md` (not in
  `GEMINI.md` or `*.instructions.md`). Edits load at session start only.
- **Combination semantics (CLI):** all applicable files are merged,
  exact duplicates deduped, and **no general precedence order is
  defined** — the CLI doc says so explicitly and tells users to avoid
  conflicts.
- **Docs disagreement (do not flatten):** the github.com customization
  docs publish a precedence chain — personal > repository >
  organization, and within a repo path-specific > repo-wide > agent
  instructions. The CLI doc publishes merge-with-no-precedence. Both
  are GitHub's; they describe different surfaces. Any claim of
  "Copilot's precedence" that doesn't name its surface is wrong.
- **Cost note (binary forensics):** Copilot injects the repo `AGENTS.md`
  into the assembled system prompt — measured ≈ +10k chars (~2.8k
  tokens) when present. Instruction files are context rent on this
  tool, paid every session.
- `COPILOT.md` as an instruction file: REFUTED (absent from the
  documented list).

**Claude Code equivalent:** partial. Claude loads `CLAUDE.md` with a
defined order plus native `AGENTS.md` fallback (≥ v2.1.277, only when
no `CLAUDE.md`); Copilot reads `CLAUDE.md` as a crossover.
**Adapter verdict:** `AGENTS.md` is the shared layer — both tools read
it natively, so canonical instructions go there. Tool annexes stay
tool-native: `.github/muse-instructions.md` + `.github/instructions/`
on the Copilot side, `CLAUDE.md`-only content on the Claude side.
Path-scoped `*.instructions.md` has no Claude equivalent at the
instruction layer (nearest equivalent: `.claude/rules/`, which Copilot
also reads).

URLs: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions ·
full survey: `hidden_files/research/instructions-files.md` §3

## Summary — canonical→adapter mapping classes

| Surface | Copilot target | Claude target | Mapping |
|---|---|---|---|
| Skills | `.github/skills/`, `.agents/skills/`, `.claude/skills/`; `~/.copilot/skills/` | `.claude/skills/`, `~/.claude/skills/` | **Direct** — one placement can serve both |
| MCP (project) | `.mcp.json` or `.github/mcp.json` | `.mcp.json` | **Direct** at project scope |
| MCP (user) | `~/.copilot/mcp-config.json` | `~/.claude.json` | Render — same schema, two files |
| Custom agents | `.github/agents/*.agent.md`; `~/.copilot/agents/` | `.claude/agents/*.md`; `~/.claude/agents/` | Render — frontmatter differs per tool |
| Plugins | `plugin.json` (+ Agent Plugins 1.0 `$schema`) | `.claude-plugin/plugin.json` | Render — portable core: skills + MCP only |
| Hooks | `.github/hooks/*.json`, settings `hooks` key | `settings.json` hooks | Render per-event; failure semantics diverge |
| Instructions | `AGENTS.md` + `.github/muse-instructions.md` + `*.instructions.md` | `AGENTS.md` (fallback) + `CLAUDE.md` | Shared layer direct; annexes tool-native |
| Instructions precedence | Merge, no order (CLI) | Defined load order | Not mappable — behavioral difference, document it |

Net: no Copilot surface is tool-native only. Every surface accepts an
externally placed file or a declarative settings entry, so the
canonical→adapter architecture covers Copilot completely. The two real
divergences a setup tool must encode are behavioral, not structural:
(1) directory trust gates repo hooks/MCP/skills/plugins in prompt
mode; (2) `postToolUseFailure` does not mean what it means in Claude
Code for shell tools.

## Correction addendum — 2026-09-30 (docs fact-check + external signal)

- §2 misattributes agent name-collision precedence: the CLI config-dir reference actually says PERSONAL wins; the "lowest level wins" statement lives in the cross-surface custom-agents-configuration reference. The disagreement between GitHub docs is real; the attribution above is wrong.
- Precedence is no longer undocumented: the Copilot CLI plugin reference states first-loaded-wins for agents and skills, LAST-loaded-wins for MCP servers. Retire "no reliable precedence"; keep the never-duplicate-names rule.
- `sessionEnd` hook output is NOT processed by Copilot (hooks reference): cleanup hooks can run commands but cannot inject context. Reinforces "automatic cleanup UNPROVEN."
- Copilot CLI v1.0.86 (2026-09-17): repo instruction files are opt-in for custom agents via `include-custom-instructions: true`.
