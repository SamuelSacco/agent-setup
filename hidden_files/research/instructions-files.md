# Agent instruction files — current state (researched 2026-09-30)

Scope: AGENTS.md, CLAUDE.md / Claude Code memory, and GitHub Copilot custom instructions across CLI, IDE, and cloud surfaces. Primary sources preferred; access date for all web sources is 2026-09-30 unless a source itself carries an earlier publication date.

## Executive takeaway

- `AGENTS.md` is now the shared instruction layer: plain Markdown, no required schema, read natively by Codex, Copilot (CLI, IDE, cloud agent / code review), Cursor, Gemini CLI, Jules, Devin, and others.
- Claude Code was the holdout. That changed on **2026-09-18** in **Claude Code v2.1.277**: with no `CLAUDE.md` / `CLAUDE.local.md` in the working directory or above it, Claude Code now reads `AGENTS.md` instead. If a `CLAUDE.md` exists, Claude reads `CLAUDE.md` only by default. A `/config` **Project instructions** setting can make it read both, only `CLAUDE.md`, or managed instructions only.
- Copilot still has its own native layer on top: `.github/muse-instructions.md` (repo-wide) and `.github/instructions/**/*.instructions.md` (path-specific, `applyTo` globs). On github.com, precedence is personal > repository (path-specific > repo-wide > agent) > organization. Copilot CLI instead *combines* applicable files and documents no general precedence order.
- Unification is real but shallow: instruction *text* is converging on `AGENTS.md`; permissions, hooks, sandboxing, skills layout, and enforcement are not unified.

---

## 1. AGENTS.md — who reads it natively, format, recent changes

### Format

- A plain Markdown file, conventionally at repo root, with nested `AGENTS.md` files allowed in subdirectories. No required fields, no enforced schema; agents read the prose. Think "README for agents": dev environment tips, testing instructions, PR instructions.
- Sources:
  - AGENTS.md site / spec repo: https://agents.md and https://github.com/agentsmd/agents.md (repo created 2025-08-19).

### Native readers (primary sources)

- **OpenAI Codex (CLI and code review)** — PROVEN. Codex builds an instruction chain at start of each run/session:
  - Global scope: `~/.codex/AGENTS.override.md` if present, else `~/.codex/AGENTS.md` (first non-empty file only).
  - Project scope: from project/Git root down to cwd, checking per directory `AGENTS.override.md`, then `AGENTS.md`, then fallback names from `project_doc_fallback_filenames` (config in `~/.codex/config.toml`); at most one file per directory.
  - Merge: concatenated root → cwd, later (closer) files override earlier guidance because they appear later. Empty files skipped; combined size capped by `project_doc_max_bytes` (32 KiB default).
  - Source: OpenAI, "Custom instructions with AGENTS.md" — https://developers.openai.com/codex/guides/agents-md
- **GitHub Copilot** — PROVEN, surface-dependent detail in §3 below. GitHub docs list `AGENTS.md` as "agent instructions" for Copilot on github.com, in IDEs, and in Copilot CLI. Nearest `AGENTS.md` in the directory tree takes precedence on github.com / cloud agent.
  - Sources: https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions ; https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
- **Claude Code** — PROVEN as of v2.1.277 (2026-09-18), conditional; see §2.
- **Others named by the Linux Foundation at AAIF launch**: Amp, Cursor, Devin, Factory, Gemini CLI, Jules, VS Code, and GitHub Copilot "among others"; AGENTS.md "adopted by more than 60,000 open source projects."
  - Source: Linux Foundation press release, 2025-12-09 — https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation

### Recent changes

- **2025-08**: AGENTS.md released by OpenAI (with the agentsmd/agents.md repo created 2025-08-19).
- **2025-12-09**: OpenAI contributed AGENTS.md to the newly formed **Agentic AI Foundation (AAIF)** under the Linux Foundation, alongside Anthropic's MCP and Block's goose. Platinum members listed: AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI.
- **2026-09-18**: Claude Code v2.1.277 added AGENTS.md support (see §2), removing the last major holdout.

---

## 2. CLAUDE.md — Claude Code instruction handling and AGENTS.md

Primary source for this whole section: Anthropic, "How Claude remembers your project" — https://code.claude.com/docs/en/memory (accessed 2026-09-30). Changelog: https://code.claude.com/docs/en/changelog

### Does Claude Code read AGENTS.md?

**Current answer (post-2026-09-18): yes, conditionally — not a blanket "never," not a blanket "always."**

Anthropic's documented default-resolution table:

| Repository state | Claude reads |
| --- | --- |
| `AGENTS.md`, and no `CLAUDE.md` or `CLAUDE.local.md` in working directory or above it | `AGENTS.md` |
| `AGENTS.md` plus a `CLAUDE.md` or `CLAUDE.local.md` in working directory or above it | `CLAUDE.md` files only |
| `CLAUDE.md` that imports `AGENTS.md` | `CLAUDE.md`, with `AGENTS.md` included through the import |

Details that matter:

- The check is about `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` in the working directory or any directory above it. `~/.claude/CLAUDE.md`, an organization's managed `CLAUDE.md`, and `.claude/rules/` files do **not** count against AGENTS.md and keep loading alongside it.
- At session start Claude reads every `AGENTS.md` and `.claude/AGENTS.md` in the working directory and ancestors; interactive sessions print a line like `no CLAUDE.md found; AGENTS.md loaded: /home/you/repo/AGENTS.md`.
- Subdirectory `AGENTS.md` files load on demand when Claude reads files there, if that subdirectory has none of the three CLAUDE files of its own.
- Inside a natively read `AGENTS.md`, `@path` imports are expanded and `claudeMdExcludes` applies. `AGENTS.local.md`, `AGENTS.override.md`, and anything under `.agents/` are **not** read.
- Version gates: requires **v2.1.277+**; unavailable if the built-in `agents-md` plugin is disabled; may not appear in the first session after upgrading from ≤ v2.1.276; before v2.1.281 some sessions (e.g. Amazon Bedrock, telemetry disabled) read CLAUDE.md only. The v2.1.277 changelog entry adds: "not yet on Bedrock, Vertex or Foundry."
  - Changelog source: https://code.claude.com/docs/en/changelog (entry "2.1.277", September 18, 2026: "Added AGENTS.md support: in a project with no CLAUDE.md, Claude Code reads AGENTS.md instead; change it under 'Project instructions' in `/config` (not yet on Bedrock, Vertex or Foundry)").

### Choosing which files load: "Project instructions" setting

Set via `/config` in-session, or in settings under the built-in `agents-md` plugin's ID in `pluginConfigs` (`~/.claude/settings.json`, a `--settings` file, or managed settings; ignored in project/local settings):

| Value | Behavior |
| --- | --- |
| `claude-md-or-agents-md` (default) | CLAUDE.md files, or AGENTS.md files when no CLAUDE.md/CLAUDE.local.md in cwd or above |
| `claude-md-and-agents-md` | Both together; per directory, CLAUDE.md files first, then AGENTS.md; an AGENTS.md already loaded via import/symlink is not read twice |
| `claude-md` | CLAUDE.md files only |
| `managed-only` | Only the org's managed CLAUDE.md + auto memory at launch; project/local/user CLAUDE.md, `.claude/rules/`, and AGENTS.md excluded (subdirectory CLAUDE.md/rules still load on read) |

### Import directives and symlinks (still supported, still the escape hatch)

- `CLAUDE.md` can import files with `@path/to/import`; imports expand into context at launch, relative paths resolve against the containing file, recursion up to **four hops**. Import parsing skips code spans and fenced blocks (wrap in backticks to mention without importing).
- `CLAUDE.md` containing only `@AGENTS.md` (+ optional Claude-specific sections below) remains Anthropic's recommended bridge when Claude is not reading AGENTS.md directly (existing CLAUDE.md, `claude-md` mode, or sessions that can't load AGENTS.md). Keeping the import never double-loads AGENTS.md.
- Symlink alternative: `ln -s AGENTS.md CLAUDE.md`. Caveats: Claude Code's Edit/Write tools refuse to write through a symlink (they redirect to the target); on Windows symlinks need Administrator/Developer Mode and Git checks a committed symlink out as a plain text file unless `core.symlinks` is enabled — so prefer `@AGENTS.md` import on Windows.
- Verify loading with `/context` (file should appear under **Memory files**).
- Migration helpers: `/init` reads Cursor rules (`.cursor/rules/`, `.cursorrules`) and Copilot rules (`.github/muse-instructions.md`); with `CLAUDE_CODE_NEW_INIT=1` it also reads `AGENTS.md`, `.devin/rules/`, `.windsurf/rules/`/`.windsurfrules`, `.clinerules`. `/import` (v2.1.213+) appends a one-time copy of files such as `AGENTS.md` into the matching `CLAUDE.md` and carries over MCP servers, commands, subagents, and skills.

### Differences when AGENTS.md is read natively vs through CLAUDE.md

Per Anthropic's comparison table:

- `InstructionsLoaded` hooks: fire for CLAUDE.md; do **not** fire for a natively read AGENTS.md (they do fire for an AGENTS.md imported/symlinked by a CLAUDE.md).
- `--add-dir` with `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` set: additional directories' CLAUDE.md loads; their AGENTS.md does not.
- External `@path` imports from AGENTS.md: load only if external imports were already approved for the project, with no prompt; from CLAUDE.md Claude asks for approval first.

Cleanup guidance if you had a pre-2.1.277 workaround: `@AGENTS.md` import can stay (never double-loads); a prose "read AGENTS.md" CLAUDE.md should be deleted or replaced with an import; a symlinked CLAUDE.md can stay or be deleted; a `SessionStart` hook printing AGENTS.md should be removed (it would add a second copy).

### CLAUDE.md file family and load order

From broadest to most specific (concatenated, not overriding; closer-to-cwd content reads last):

1. **Managed policy**: `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS), `/etc/claude-code/CLAUDE.md` (Linux/WSL), `C:\Program Files\ClaudeCode\CLAUDE.md` (Windows). Cannot be excluded. Managed settings can also embed content via the `claudeMd` key in `managed-settings.json` (honored only in managed/policy settings).
2. **User**: `~/.claude/CLAUDE.md`.
3. **Project**: `./CLAUDE.md` or `./.claude/CLAUDE.md` (team-shared via source control).
4. **Local**: `./CLAUDE.local.md` — personal, gitignored, appended after CLAUDE.md at the same level; exists only in the worktree where created (share across worktrees by importing from home).

Load mechanics:

- CLAUDE.md and CLAUDE.local.md from cwd and every ancestor load at launch; subdirectory files load on demand when Claude reads files there.
- `--add-dir` directories do not load memory files unless `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` is set.
- Block-level HTML comments (`<!-- ... -->`) in CLAUDE.md are stripped before injection into context.
- `claudeMdExcludes` (user/project/local/managed settings) skips files by absolute path or glob — monorepo escape hatch; managed-policy CLAUDE.md cannot be excluded.
- Guidance: target under 200 lines per CLAUDE.md; instructions are context, not enforced configuration (use hooks/settings for hard blocks). `/doctor prompt-audit` (v2.1.283+) audits CLAUDE.md, CLAUDE.local.md, AGENTS.md, and `.claude/` rules/skills/commands/subagents/output-styles for outdated or conflicting instructions.

### `.claude/rules/` — modular, path-scoped rules

- Markdown files under project `.claude/rules/` (recursive, subdirectories allowed) or user-level `~/.claude/rules/` (applies to every project; loaded before project rules).
- Rules **without** frontmatter load at launch with the same priority as `.claude/CLAUDE.md`. Rules with YAML frontmatter `paths:` (glob list or comma-separated string; brace expansion supported) load only when Claude works with matching files — as of v2.1.198 matching works through symlinked project paths. `paths` is the only frontmatter field Claude reads from a rule; unparseable frontmatter means the rule loads unscoped.
- Symlinks are supported for sharing rules across projects; a symlink target outside the working directory is treated like an external import (approval flow), path-scoped linked rules don't load until approved. User-level `~/.claude/rules/` avoids the approval path.
- Behavior note: before v2.1.211, on-demand rules loaded even when `project` was excluded from setting sources; now project rules are skipped when `project` is excluded.

### Output styles interplay

Primary source: Anthropic, "Output styles" — https://code.claude.com/docs/en/output-styles (accessed 2026-09-30).

- An output style sets role/tone/response format for **every response in a session** — a different layer from CLAUDE.md: CLAUDE.md holds what Claude should *know* about the codebase and "stays loaded whichever style you pick"; a style shapes *how* it responds. Anthropic's own decision table routes project conventions/commands/structure to CLAUDE.md, session-wide voice/format to an output style, single-task procedures to a skill, guaranteed behavior to a hook, focused helpers to a subagent, and CLI-passed additions to `--append-system-prompt`.
- Built-ins beyond Default: **Proactive**, **Concise** (v2.1.237+), **Explanatory**, **Learning** — each keeps the default software-engineering instructions and adds its own.
- Switch via `/output-style <style>` (v2.1.269+), `/config` → Output style, VS Code command menu (v2.1.257+), or the `outputStyle` settings field (case-sensitive; saved to `.claude/settings.local.json` by the pickers; `~/.claude/settings.json` for a cross-project default; project settings override user). Mid-session switches apply from the next message (before v2.1.251 they needed `/clear` or a new session).
- Custom styles: Markdown with optional frontmatter (`name`, `description`, `keep-coding-instructions`, `force-for-plugin`). Critical gotcha: a custom style **drops Claude Code's built-in software-engineering instructions unless `keep-coding-instructions: true`**. Plugins can ship styles in an `output-styles/` directory; `force-for-plugin: true` auto-applies when the plugin is enabled.
- Scope: styles apply to the main conversation and to a fork (which inherits the parent's system prompt); other subagents run their own system prompts and are unaffected. Style instructions are sent with every request (prompt caching offsets repeat cost); Explanatory/Learning lengthen output by design, Concise shortens it.

---

## 3. GitHub Copilot instructions — current structure

Primary sources: GitHub Docs —
- "Adding repository custom instructions for GitHub Copilot" — https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions
- "Adding repository custom instructions for GitHub Copilot in your IDE" — https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide
- "Adding custom instructions for GitHub Copilot CLI" — https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
- "About customizing GitHub Copilot responses" — https://docs.github.com/en/copilot/concepts/prompting/response-customization

### The three repository instruction types

1. **Repository-wide**: `.github/muse-instructions.md` — applies to all requests in the repo context. Available as soon as the file is saved; in Copilot Chat the file shows in the response's References when used.
2. **Path-specific**: `NAME.instructions.md` files in or below `.github/instructions/`, with YAML frontmatter:
   - `applyTo`: glob (comma-separated for multiple patterns; `**` matches everything).
   - `excludeAgent`: `"code-review"` or `"cloud-agent"` to opt out of one consumer; absent means both use it.
   - If a path-specific file matches and a repo-wide file exists, both are used.
   - Surface caveat (github.com): "Currently, on GitHub.com, path-specific custom instructions are only supported for Copilot cloud agent and Copilot code review." VS Code supports them in IDE; Copilot CLI includes modular files when `applyTo` matches a file being worked on.
3. **Agent instructions**: one or more `AGENTS.md` files **anywhere** in the repository — "the nearest `AGENTS.md` file in the directory tree will take precedence." Alternatively a single root `CLAUDE.md` or `GEMINI.md`.

### Precedence (github.com surfaces)

From "About customizing GitHub Copilot responses": personal > repository > organization, and within repository: path-specific > repo-wide > agent instructions. But "all sets of relevant instructions are provided to Copilot" — precedence resolves conflicts, it does not drop the losing files. GitHub also cautions that output is non-deterministic, so instructions are followed approximately, not mechanically.

### Copilot CLI specifics (differs from github.com!)

Copilot CLI discovers instructions in the repo root, cwd, intermediate directories, and directories in the path of files being worked on:

| Location | Scope |
| --- | --- |
| `$HOME/.copilot/copilot-instructions.md` | User-level, across repos (`COPILOT_HOME` overrides `$HOME/.copilot`) |
| `$HOME/.copilot/instructions/**/*.instructions.md` | Modular user-level |
| `.github/muse-instructions.md` | Repo-wide |
| `.github/instructions/**/*.instructions.md` | Modular repo instructions (not discovered in intermediate directories) |
| `AGENTS.md` | Agent instructions |
| `CLAUDE.md` (also `.claude/CLAUDE.md`) | Agent instructions |
| `GEMINI.md` | Agent instructions |
| Directories in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Additional `AGENTS.md` and `*.instructions.md` |

- **Combination, not precedence**: "When multiple applicable user-level and repository instruction files exist, Copilot CLI combines their instructions… but does not define a general precedence order between these files. Avoid conflicting instructions." (Identical user-level/repo/agent files are de-duplicated.) This is a genuine behavioral difference from the documented github.com precedence list — do not present one order as "Copilot's order" without naming the surface.
- `@` file references: in `.github/muse-instructions.md`, `AGENTS.md`, or `CLAUDE.md`, `@relative/path` includes another file immediately (nesting supported). Referenced files must stay within the repo (or the custom-instructions dir for local files); absolute paths and `~/` are not loaded; references are not expanded in `GEMINI.md` or `*.instructions.md`.
- `/instructions` in the CLI lists discovered instruction files for the session and lets you enable/disable individual files. Edits to instruction files are not picked up mid-session — exit and resume (`copilot --continue`) or start a new session (`/new`).

### IDE specifics

- VS Code supports all three types; note: "Support of `AGENTS.md` files outside of the workspace root is currently turned off by default" (enable via VS Code custom-instructions settings). Custom instructions are enabled by default and can be toggled per user ("Code Generation: Use Instruction Files"); usage is visible in the Chat References list.
- Visual Studio documentation covers repo-wide + path-specific only (no AGENTS.md in its supported-types list) — surface differences persist even among IDEs.
- Path-specific instructions do not apply to Copilot Chat in the IDE on github.com surfaces; anything the IDE chat must see belongs in `.github/muse-instructions.md`. (Per GitHub docs notes above; treat surface claims individually.)

### Recommended structure (from GitHub's docs, consolidated)

- Put shared, cross-tool standing rules in root `AGENTS.md` (nearest-wins for nested overrides).
- Put Copilot-only repo-wide guidance in `.github/muse-instructions.md`; keep it short, self-contained statements (project overview, coding standards, frameworks/versions) — it is sent with every request.
- Put scoped rules in `.github/instructions/*.instructions.md` with tight `applyTo` globs; use `excludeAgent` only when a rule should not reach code review or the cloud agent.
- Keep personal preferences at user level (Copilot CLI: `$HOME/.copilot/copilot-instructions.md`; github.com Chat: personal instructions setting). Org-wide rules need Copilot Business/Enterprise (organization instructions).
- Avoid conflicts across layers: everything relevant is sent, conflicting text costs tokens and consistency.

---

## 4. Movement toward unification

**PROVEN for the instruction-text layer; REFUTED as a claim about the whole configuration surface.**

Evidence for convergence:

- AGENTS.md began as an OpenAI-led convention (Aug 2025; co-signed in practice by the Amp/Jules/Cursor/Factory ecosystem) and was contributed to the **Agentic AI Foundation (AAIF)** under the Linux Foundation on **2025-12-09**, with MCP (Anthropic) and goose (Block) as sibling founding projects. The LF describes AGENTS.md as "a simple, universal standard that gives AI coding agents a consistent source of project-specific guidance… across different repositories and toolchains," already adopted by 60,000+ projects and by Amp, Codex, Cursor, Devin, Factory, Gemini CLI, GitHub Copilot, Jules, and VS Code.
  - Source: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
- Copilot reads other vendors' files outright: `AGENTS.md` anywhere, and root `CLAUDE.md` / `GEMINI.md` as alternatives; Copilot CLI also reads `.claude/CLAUDE.md`.
- Claude Code joined the standard on **2026-09-18** (v2.1.277) with conditional native AGENTS.md reading plus a `/config` "Project instructions" mode to read both files together.
- Codex keeps its own discovery rules (global + per-directory chain, `AGENTS.override.md`, fallback filenames, 32 KiB cap) but on the same `AGENTS.md` filename.
- Tooling is emerging to generate per-tool adapters (e.g. `CLAUDE.md` = `@AGENTS.md` import or symlink) from one canonical file — community practice, consistent with both vendors' docs.

Limits of unification:

- Discovery and precedence semantics still differ per tool: Codex concatenates root→cwd with a byte cap; Claude loads CLAUDE.md ancestors at launch and subdirectories on demand, with AGENTS.md conditional on CLAUDE.md absence (by default); Copilot on github.com uses nearest-AGENTS.md + an explicit precedence list, while Copilot CLI combines without a defined precedence order.
- AGENTS.md is deliberately instruction-only: it does not standardize permissions, hooks, sandboxing, or enforcement. Claude Code remains CLAUDE.md-first whenever a CLAUDE.md exists, and its `.claude/rules/`, output styles, auto memory, and managed-policy layer have no cross-tool equivalents.
- Surface fragmentation inside a single vendor persists (GitHub: github.com vs CLI vs VS Code vs Visual Studio all support slightly different subsets).

---

## Claim checks

| # | Claim | Verdict | Basis |
| --- | --- | --- | --- |
| 1 | AGENTS.md is plain Markdown with no required schema | PROVEN | https://agents.md ; https://github.com/agentsmd/agents.md |
| 2 | Codex reads AGENTS.md natively (global `~/.codex`, per-directory chain, `AGENTS.override.md`, fallback names, 32 KiB cap) | PROVEN | https://developers.openai.com/codex/guides/agents-md |
| 3 | Copilot CLI reads AGENTS.md natively | PROVEN | https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions |
| 4 | Copilot (cloud agent / code review / IDE) reads AGENTS.md, nearest in tree wins | PROVEN | https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions |
| 5 | "Claude Code does not read AGENTS.md" (blanket, present tense) | REFUTED (outdated) | True before v2.1.277; refuted by Anthropic memory docs + changelog entry for 2.1.277 (2026-09-18): https://code.claude.com/docs/en/memory ; https://code.claude.com/docs/en/changelog |
| 6 | Claude Code reads AGENTS.md when no CLAUDE.md/CLAUDE.local.md exists in cwd or above (default mode) | PROVEN | https://code.claude.com/docs/en/memory (resolution table + "When Claude Code reads AGENTS.md") |
| 7 | Claude Code can be set to read both CLAUDE.md and AGENTS.md (`claude-md-and-agents-md`) | PROVEN | Same Anthropic memory doc, "Choose which instruction files load" |
| 8 | `@AGENTS.md` import inside CLAUDE.md works and never double-loads | PROVEN | Same doc, "Share one file with other coding tools" |
| 9 | Symlinking CLAUDE.md → AGENTS.md works (with Windows/Edit-tool caveats) | PROVEN | Same doc |
| 10 | CLAUDE.local.md exists for personal, gitignored project instructions | PROVEN | Same doc (locations table; "Import additional files") |
| 11 | `.claude/rules/` supports path-scoped rules via `paths` frontmatter | PROVEN | Same doc, "Organize rules with `.claude/rules/`" |
| 12 | Output styles are a separate layer from CLAUDE.md (session-wide response shaping; custom styles drop built-in coding instructions unless `keep-coding-instructions: true`) | PROVEN | https://code.claude.com/docs/en/output-styles |
| 13 | Copilot repo-wide instructions live in `.github/muse-instructions.md`; path-specific in `.github/instructions/*.instructions.md` with `applyTo` / `excludeAgent` | PROVEN | https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions |
| 14 | Path-specific `*.instructions.md` apply on every Copilot surface | REFUTED (surface-dependent) | GitHub docs: on github.com they are supported only for cloud agent and code review; IDE/CLI support differs. Same source as #13; CLI: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions |
| 15 | Copilot precedence: personal > repository (path-specific > repo-wide > agent) > organization | PROVEN (github.com surfaces) | https://docs.github.com/en/copilot/concepts/prompting/response-customization |
| 16 | Copilot CLI resolves conflicts by that same precedence order | REFUTED | CLI docs state the CLI "combines their instructions" and "does not define a general precedence order between these files": https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions |
| 17 | Copilot also accepts root `CLAUDE.md` / `GEMINI.md`, and the CLI also reads `.claude/CLAUDE.md` | PROVEN | GitHub Docs sources in §3 |
| 18 | AGENTS.md is stewarded by the Agentic AI Foundation under the Linux Foundation (contributed 2025-12-09 with MCP and goose) | PROVEN | https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation |
| 19 | "60,000+ projects use AGENTS.md; 20–30+ tools read it" | UNVERIFIABLE (independently) | Figure originates with OpenAI/Linux Foundation (Dec 2025 press release). No independent audit found in primary sources; fine to cite as "per the Linux Foundation," not as a measured fact. |
| 20 | AGENTS.md unifies agent configuration (permissions, hooks, sandbox, enforcement) | REFUTED | AGENTS.md is instruction-text only; Claude Code routes enforcement to hooks/settings, Copilot/Codex keep tool-specific config. See §4 limits. |

## Presentation-safe summary lines

- "Write shared project rules once in `AGENTS.md`. Codex and Copilot read it natively; since 2026-09-18 Claude Code reads it too — provided no `CLAUDE.md` sits in the directory or above it."
- "If you keep a `CLAUDE.md`, make its first line `@AGENTS.md` and add Claude-only notes below. One source of truth, no drift, no double-load."
- "Copilot keeps two native extras: `.github/muse-instructions.md` for repo-wide Copilot guidance and `.github/instructions/*.instructions.md` for glob-scoped rules. On github.com those outrank AGENTS.md; in Copilot CLI everything is merged with no defined precedence — so don't write conflicting rules and expect a referee."
- "Unification covers the instruction text. Permissions, hooks, and sandboxing are still per-tool — budget adapter files for those."

## Sources (all accessed 2026-09-30)

- Anthropic — How Claude remembers your project: https://code.claude.com/docs/en/memory
- Anthropic — Claude Code changelog (2.1.277, September 18, 2026): https://code.claude.com/docs/en/changelog
- Anthropic — Output styles: https://code.claude.com/docs/en/output-styles
- OpenAI — Custom instructions with AGENTS.md (Codex): https://developers.openai.com/codex/guides/agents-md
- GitHub Docs — Adding repository custom instructions for GitHub Copilot: https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions
- GitHub Docs — Adding repository custom instructions in your IDE: https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide
- GitHub Docs — Adding custom instructions for GitHub Copilot CLI: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
- GitHub Docs — About customizing GitHub Copilot responses: https://docs.github.com/en/copilot/concepts/prompting/response-customization
- AGENTS.md project: https://agents.md ; https://github.com/agentsmd/agents.md
- Linux Foundation — AAIF formation press release (2025-12-09): https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
