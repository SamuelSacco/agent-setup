# Claude Code — official documentation verification

Date checked: 2026-09-30. Sources: official pages on code.claude.com only. No CLI run, no API spend. Each claim gets a verdict (PROVEN / REFUTED / UNVERIFIABLE), the deciding URL, and the exact sentence that decides it.

## 1. Telemetry switches — PROVEN

URL: https://code.claude.com/docs/en/monitoring-usage

- “`CLAUDE_CODE_ENABLE_TELEMETRY` | Enables telemetry collection (required) | `1`”
- “`OTEL_LOGS_EXPORTER` | Logs/events exporter types, comma-separated. Use `none` to disable | `console`, `otlp`, `none`”

So `CLAUDE_CODE_ENABLE_TELEMETRY=1` turns telemetry on and `OTEL_LOGS_EXPORTER=console` is a documented exporter value. Placement matters: “Claude Code ignores the OpenTelemetry exporter variables in a repository's `.claude/settings.json` and `.claude/settings.local.json`, so a repository can't use them to turn telemetry on, choose where it goes, or capture content.” Set them in managed settings, the shell, or `~/.claude/settings.json`. OTel config is read at startup; relaunch after changing it.

## 2. Raw API-body capture — PROVEN

URL: https://code.claude.com/docs/en/monitoring-usage

- “`OTEL_LOG_RAW_API_BODIES` | Emit the full Anthropic Messages API request and response JSON as `api_request_body` / `api_response_body` log events (default: disabled). Bodies include the entire conversation history. Enabling this implies consent to everything `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_DETAILS`, and `OTEL_LOG_TOOL_CONTENT` would reveal | `1` for inline bodies truncated at the content limit (60 KB by default), or `file:<dir>` for untruncated bodies on disk with a `body_ref` pointer in the event”
- Request `body`: “JSON-serialized Messages API request parameters, such as the system prompt, messages, and tools, truncated at the content limit (60 KB by default). Extended-thinking content in prior assistant turns is redacted. Emitted only in inline mode (`OTEL_LOG_RAW_API_BODIES=1`).”
- File mode: “`body_ref`: Absolute path to a `<dir>/<uuid>.request.json` file containing the untruncated body. Emitted only in file mode (`OTEL_LOG_RAW_API_BODIES=file:<dir>`).” The response side mirrors this with `<dir>/<request_id>.response.json`.
- Index: “In file mode (`OTEL_LOG_RAW_API_BODIES=file:<dir>`), Claude Code also appends one JSON line to `<dir>/index.jsonl` for each successful response, with the fields `timestamp`, `session_id`, `query_source`, `model`, `request_id`, `message_id`, `message_uuid`, `request_file`, and `response_file`.” The index requires Claude Code v2.1.274 or later.

Terminology: the docs say “JSON-serialized Messages API request parameters” and response JSON. That is serialized API JSON, not a byte-for-byte HTTP wire capture; don't claim the latter.

## 3. Hook events: PostToolUse vs PostToolUseFailure — PROVEN

URL: https://code.claude.com/docs/en/hooks

- “`PostToolUse` | After a tool call succeeds”
- “`PostToolUseFailure` | After a tool call fails”

They are distinct events. Routing failures to `PostToolUseFailure` (not `PostToolUse`) is correct. The same page's lifecycle table lists the full event set: SessionStart, Setup, UserPromptSubmit, UserPromptExpansion, PreToolUse, PermissionRequest, PermissionDenied, PostToolUse, PostToolUseFailure, PostToolBatch, Notification, MessageDisplay, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, TeammateIdle, InstructionsLoaded, ConfigChange, CwdChanged, DirectoryAdded, FileChanged, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact, PreModelSwitch, PostModelSwitch, Elicitation, ElicitationResult, SessionEnd.

## 4. CLAUDE.md hierarchy and loading — PROVEN

URL: https://code.claude.com/docs/en/memory

Load order (broadest to most specific): managed policy `CLAUDE.md`; user `~/.claude/CLAUDE.md`; project `./CLAUDE.md` or `./.claude/CLAUDE.md`; local `./CLAUDE.local.md`.

- “The table below lists them in load order, from broadest scope to most specific, so a project instruction appears in context after a user instruction.”
- “CLAUDE.md and CLAUDE.local.md files in the directory hierarchy above the working directory are loaded at launch. Files in subdirectories load on demand when Claude reads files in those directories.”
- “All discovered files are concatenated into context rather than overriding each other.”
- “Across the directory tree, content is ordered from the filesystem root down to your working directory.”
- “Within each directory, `CLAUDE.local.md` is appended after `CLAUDE.md`.”

Project rules live in `.claude/rules/`; all `.md` files are discovered recursively. Rules without `paths` load at launch; path-scoped rules load when Claude reads matching files: “Rules without a `paths` field are loaded unconditionally and apply to all files. Path-scoped rules trigger when Claude reads files matching the pattern, not on every tool use.”

## 5. Imports, including `@AGENTS.md` — PROVEN

URL: https://code.claude.com/docs/en/memory

- “CLAUDE.md files can import additional files using `@path/to/import` syntax. Imported files are expanded and loaded into context at launch alongside the CLAUDE.md that references them.”
- “Both relative and absolute paths are allowed. Relative paths resolve relative to the file containing the import, not the working directory. Imported files can recursively import other files, with a maximum depth of four hops.”

`@AGENTS.md` is an explicitly supported import: “you can still keep it as the one file every tool shares by putting an `@AGENTS.md` import in a `CLAUDE.md` next to it... Add any Claude-specific instructions below the import, and Claude reads the imported file first, then the rest.”

## 6. Native AGENTS.md support — PROVEN, with version caveat

URL: https://code.claude.com/docs/en/memory

- “Claude Code can read `AGENTS.md` as your project instructions, so a repository already set up for other coding agents works without adding a `CLAUDE.md`, an import, or a setting.”
- “By default, Claude reads `AGENTS.md` only when you have no `CLAUDE.md` in your working directory or above it.”
- Default selection: AGENTS.md alone → “Your `AGENTS.md`”; AGENTS.md plus a CLAUDE.md or CLAUDE.local.md → “Your `CLAUDE.md` files only”; an importing CLAUDE.md → “Your `CLAUDE.md`, with `AGENTS.md` included through the import”.
- “At session start: every `AGENTS.md` and `.claude/AGENTS.md` in your working directory and the directories above it.”
- Version floor: AGENTS.md support is unavailable when “You're on a Claude Code version before v2.1.277.”
- Caveat: “Before v2.1.281, some sessions, such as those on Amazon Bedrock or with telemetry disabled, read `CLAUDE.md` files only. On those versions, update Claude Code. To give Claude your `AGENTS.md` in any of these sessions, import it from a `CLAUDE.md`.”

So: native AGENTS.md since v2.1.277 when no Claude-specific file supersedes it — PROVEN. For dependable behavior across Bedrock and telemetry-disabled sessions, run v2.1.281+ or keep a `CLAUDE.md` containing `@AGENTS.md`.

## 7. Settings precedence — PROVEN

URL: https://code.claude.com/docs/en/settings

- “When the same key appears in more than one place, Claude Code uses the value from the highest level that sets it.”

Highest to lowest: (1) Managed settings; (2) Command line arguments, including `--settings`; (3) Project local `.claude/settings.local.json`; (4) Shared project `.claude/settings.json`; (5) User `~/.claude/settings.json`.

- “Environment variables aren't a level in this stack. When a behavior has both a shell variable and a settings key, which one applies is decided per pair, not by level”

List-valued keys generally merge across files instead of overriding, with documented exceptions for model lists (`fallbackModel`, `modelPicker`, `availableModels`, `modelSettings`).

## 8. Discovery: skills, subagents, plugins — PROVEN

### Skills

URL: https://code.claude.com/docs/en/skills

- Format: “Skills are configured through YAML frontmatter at the top of `SKILL.md` and the markdown content that follows.”
- Required fields: none. “All fields are optional. Only `description` is recommended so Claude knows when to use the skill.”
- Locations: managed settings directory; personal `~/.claude/skills/<name>/SKILL.md`; project `.claude/skills/<name>/SKILL.md`; nested `<subdir>/.claude/skills/<name>/SKILL.md` (loads when Claude works on files there); `--add-dir` directories; plugin `skills/` directories, invoked as `/plugin-name:skill-name`.
- “Claude Code loads project skills from `.claude/skills/` in the directory where you start it and in every parent directory up to the repository root”
- “When you add a directory with `--add-dir` or `/add-dir`, Claude Code loads the skills in that directory's `.claude/skills/`, along with its `.claude/commands/` and `.claude/agents/`.”

### Subagents

URL: https://code.claude.com/docs/en/sub-agents

- Format: “Subagents are Markdown files with YAML frontmatter.”
- “Only `name` and `description` are required.”
- “The frontmatter defines the subagent's metadata and configuration. The body becomes the system prompt that guides the subagent's behavior.”
- Locations by priority: (1) managed settings; (2) `--agents` CLI flag (session only); (3) project `.claude/agents/`; (4) user `~/.claude/agents/`; (5) plugin `agents/` directory.
- “Claude Code scans `.claude/agents/` and `~/.claude/agents/` recursively”
- Plugin subagents ignore the `hooks`, `mcpServers`, and `permissionMode` frontmatter fields: “For security reasons, plugin subagents don't support the `hooks`, `mcpServers`, or `permissionMode` frontmatter fields. These fields are ignored when loading agents from a plugin.”

### Plugins

URL: https://code.claude.com/docs/en/plugins/overview

- “A Claude Code plugin is a directory of skills, agents, hooks, MCP servers, or other components that Claude Code installs and loads as one unit.”
- “The manifest, a JSON file at `.claude-plugin/plugin.json`, gives the plugin its name and can add a version, a description, and other metadata.”
- Components load from the plugin root: `skills/<name>/SKILL.md`, `agents/*.md`, `hooks/hooks.json`, `.mcp.json`. A plugin skill runs as `/plugin-name:skill-name`.
- Installed plugins live on disk: “`~/.claude/plugins/` holds what Claude Code has fetched and installed.” Marketplaces are catalogs with a `.claude-plugin/marketplace.json`; plugins are installed and enabled, not auto-read from arbitrary project directories.
- Development without a marketplace: “While you're developing a plugin, you don't need a marketplace: load it straight from its folder with `--plugin-dir`”
- Layers before a plugin skill runs: settings list the marketplace and enabled plugins; disk holds the install under `~/.claude/plugins/`; plugins load at startup or on reload.

Corroborating file reference: https://code.claude.com/docs/en/claude-directory — “Claude Code reads instructions, settings, skills, subagents, and memory from your project directory and from `~/.claude` in your home directory.”

## Verdict summary

All eight claim families PROVEN against official docs. Two carry qualifiers: native AGENTS.md needs v2.1.277+ and is unreliable on v2.1.277–v2.1.280 for Amazon Bedrock and telemetry-disabled sessions (use v2.1.281+ or an `@AGENTS.md` import); the raw-body `index.jsonl` linkage needs v2.1.274+. Nothing REFUTED, nothing UNVERIFIABLE.
