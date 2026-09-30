# Changelog audit — Claude Code + Copilot CLI — 2026-09-30

Scope: official changelogs and official docs only, ~3–6 months back.
Claude Code: v2.1.105 (2026-04-13) → v2.1.285 (2026-09-29; installed).
Copilot CLI: ~v1.0.15 (2026-04-01) → v1.0.89 (2026-09-28; installed).
Web research only; no CLI runs; no API spend. Per item: version — date —
change — why it matters for the canonical→adapter→native bridge.

Sources: Claude Code — github.com/anthropics/claude-code CHANGELOG.md,
code.claude.com/docs/en/changelog, code.claude.com/docs/en/advisor.md,
releases/tag/v2.1.285. Copilot CLI — github.com/github/copilot-cli
changelog.md, github.blog/changelog, docs.github.com Copilot CLI reference
and hooks reference.

---

## Part 1 — Claude Code

### OpenTelemetry / logging

- v2.1.111 — 2026-04-16 — `OTEL_LOG_RAW_API_BODIES` added: full API
  request/response bodies as OTel log events. The raw-body claim Samuel
  relayed is real and predates our setup.
- v2.1.117 — 2026-04-22 — `user_prompt` events gain command fields;
  usage events gain `effort` attribute.
- v2.1.119 — 2026-04-23 — `tool_result`/`tool_decision` gain
  `tool_use_id`, `tool_input_size_bytes`.
- v2.1.139 — 2026-05-11 — Subagent spans carry agent/parent IDs
  (v2.1.145 — 2026-05-19 — `agent_id`/`parent_agent_id` on
  `claude_code.tool` spans).
- v2.1.193 — 2026-06-25 — `claude_code.assistant_response` event;
  separate content opt-ins (`OTEL_LOG_ASSISTANT_RESPONSES`).
- v2.1.217 — 2026-07-21 — Managed OTLP endpoint overrides lower settings
  scopes. Telemetry policy moved up-scope.
- v2.1.251 — 2026-08-28 — Project settings can no longer enable raw API
  bodies / detailed beta tracing or bypass a managed collector. Upstream
  enforces what our adapter already assumed: generated project config
  carries no telemetry policy.
- v2.1.274 — 2026-09-17 — `OTEL_LOG_RAW_API_BODIES=file:<dir>` improved:
  `index.jsonl` + `request_body_id`/`message.id` link response files to
  requests and transcript messages. This is the lossless capture mode
  for prompt forensics (why a harness spent N input tokens).
- v2.1.283 — 2026-09-25 — MCP/WebFetch/WebSearch output enters
  `tool.output` spans behind `OTEL_LOG_TOOL_CONTENT=1`.

Impact: exporters, raw bodies, and collectors belong in user/managed
scope only. Claude-side observability is env/managed-settings work, not
repo files. All captures off by default; three separate opt-ins.

### Hooks

- v2.1.105 — 2026-04-13 — `PreCompact` added; exit 2 /
  `{"decision":"block"}` blocks compaction.
- v2.1.118 — 2026-04-23 — Hooks can invoke MCP tools (`type: "mcp_tool"`).
- v2.1.119 — 2026-04-23 — `PostToolUse` and `PostToolUseFailure` gain
  `duration_ms`. Earliest in-window proof `PostToolUseFailure` exists.
- v2.1.121 — 2026-04-28 — `PostToolUse` can replace tool output
  (`hookSpecificOutput.updatedToolOutput`).
- v2.1.139 — 2026-05-11 — Exec-form hooks (`args: string[]`);
  `PostToolUse.continueOnBlock`.
- v2.1.251 — 2026-08-28 — New events: `PreModelSwitch`,
  `PostModelSwitch`.
- v2.1.285 — 2026-09-29 — Sync hooks no longer hang on open child output.
- Negative result: no changelog entry records when `PostToolUseFailure`
  was introduced. Changelog only proves existence by v2.1.119.

Impact: canonical hook semantics compile to Claude event names plus
stdin/stdout JSON contracts. Adapter emits `settings.json` hooks only
where a native event exists; unmapped canonical events stay canonical,
never silently dropped. Our S4 mapping (`tool_failure` →
`PostToolUseFailure`) rests on local adapter evidence, not changelog.

### AGENTS.md / instructions

- v2.1.277 — 2026-09-18 — With no `CLAUDE.md` present, Claude Code reads
  `AGENTS.md`. Configurable via `/config` → Project instructions.
- v2.1.281 — 2026-09-23 — AGENTS.md support expanded to Bedrock, Vertex
  AI, Foundry, LLM gateways, telemetry-disabled sessions. The v2.1.277
  provider restriction is historical, not current.
- Negative results: no changelog entry documents `@AGENTS.md` import
  syntax as a changelog feature; no `.agents/skills` consumption.

Impact: shared root `AGENTS.md` + `CLAUDE.md` starting `@AGENTS.md`
remains the robust bridge (ledger C4). Instruction support is real;
skill discovery did not move with it.

### Skills

- v2.1.105 — 2026-04-13 — Skill description cap 250 → 1,536 chars.
- v2.1.142 — 2026-05-14 — Plugins may ship root-level `SKILL.md`.
- v2.1.152 — 2026-05-27 — `disallowed-tools` frontmatter;
  `/reload-skills`; `SessionStart.reloadSkills`.
- v2.1.218 — 2026-07-22 — `context: fork` skills default to background.
- v2.1.283 — 2026-09-25 — `/doctor prompt-audit` audits skills, agents,
  commands, and CLAUDE.md for older-model prompting patterns.
- Negative result: no native `.agents/skills` discovery in window.

Impact: canonical skills compile to native `.claude/skills` (or plugin
trees). Claude-only frontmatter (`disallowed-tools`, `context: fork`)
is adapter-emitted, never stored in canonical form.

### Subagents / advisor

- v2.1.117 — 2026-04-22 — Advisor Tool already exists, labeled
  experimental (introduction predates window). Forked subagents via
  `CLAUDE_CODE_FORK_SUBAGENT=1`.
- v2.1.219 — 2026-07-24 — Nested subagent depth 3 by default
  (v2.1.217 concurrency changes, 2026-07-21).
- v2.1.260 — 2026-09-03 — Text form of `/advisor` (`/advisor`,
  `/advisor <model>`, `/advisor off`) for desktop, Remote Control, and
  headless sessions; docs require v2.1.260+.
- v2.1.280 — 2026-09-22 — Advisor gateway fallback when the advisor beta
  is unsupported by the gateway.
- Advisor (official docs, read 2026-09-30): server-executed tool;
  executor consults a stronger model mid-task with full transcript;
  Anthropic API only — not on Bedrock, Claude Platform on AWS, Google
  Agent Platform, or Foundry. Enabled via `/advisor`, `advisorModel`, or
  `--advisor`. Pairing validated (advisor ≥ executor capability);
  subagents inherit and re-validate. Advisor calls re-read the full
  transcript uncached; toggling does not invalidate the main prompt
  cache. Requires feature-flag fetching — telemetry/flag-disabled
  sessions keep it off. `CLAUDE_CODE_DISABLE_ADVISOR_TOOL=1` kills it.

Impact: advisor is session-level Claude config, never a canonical
agent. Grounds ledger C1 (Sonnet drives, Opus advises; not
token-neutral — advisor re-reads the transcript at advisor rates).

### Plugins

- v2.1.105 — 2026-04-13 — Top-level `monitors` manifest key.
- v2.1.145 — 2026-05-19 — `/plugin` previews commands/agents/skills/
  hooks/MCP before install; `claude plugin validate` ( `--json` added
  v2.1.259 — 2026-09-02).
- v2.1.285 — 2026-09-29 — `claude plugin configure`; install-time config
  for plugin-bundled `.mcpb` servers.

Impact: plugins distribute canonical assets; they do not author them.
Generate `plugin.json` + native trees; validate with upstream tooling.
Our `canonical/plugins/` stays an unimplemented slot until this earns
an eval.

### MCP

- Baseline: project `.mcp.json` supported and workspace-trust-gated
  throughout; introduction predates window.
- v2.1.196 — 2026-06-29 — `claude mcp list`/`get` no longer spawn
  project servers that committed settings auto-approved; untrusted
  workspaces show them pending approval.
- v2.1.259 — 2026-09-02 — `managedMcpServers` managed setting: org-wide
  HTTP/SSE servers in `.mcp.json` shape; command entries skipped.
- v2.1.274 — 2026-09-17 — `CLAUDE_CODE_MCP_STARTUP_WAIT_MS`; new MCP
  client/protocol negotiation (2026-07-28) on Bedrock/Vertex/Foundry;
  `"type": "sdk"` file entries skipped with warning.

Impact: canonical MCP compiles to `.mcp.json` at project scope. Org
distribution is a separate HTTP/SSE-only channel — stdio canonical
servers cannot ride it. `"type": "sdk"` is never written to files.

### --bare / apiKeyHelper

- Negative results: no introduction entries for either in window; both
  are stable, pre-window surfaces.
- v2.1.139 — 2026-05-11 — Remote/scheduled features disabled when
  API-key credentials (incl. `apiKeyHelper`) are active.
- v2.1.284 — 2026-09-28 — Forced-login refusal names credential source.

Impact: credential mode is a deployment-profile branch. Our
`--bare` + apiKeyHelper verification path is unaffected, but anything
relying on remote/scheduled features cannot share that profile.

### Models / effort

- v2.1.117 — 2026-04-22 — Pro/Max default effort on Opus 4.6 / Sonnet
  4.6 raised medium → high.
- v2.1.197 — 2026-06-30 — Sonnet 5 default; native 1M context.
- v2.1.219 — 2026-07-24 — Opus 5 default; 1M context.
- v2.1.251 — 2026-08-28 — `/effort` defaults become per-model.
- v2.1.280 — 2026-09-22 — Opus 5.5 default (1M ctx, $4/$20 per Mtok,
  $0.20/Mtok cache reads). Effort saved for older models does not carry
  to newly released models automatically.
- v2.1.284 — 2026-09-28 — Sonnet 5.5 default on Anthropic API (1M ctx,
  $2/$10 per Mtok, $0.20/Mtok cache reads).
- Negative result: the word "prefill" appears nowhere in the audited
  changelog. No new Haiku landed through v2.1.285; docs still pair
  against Haiku 4.5.

Impact: three default rotations in one quarter. Canonical configs pin
model family aliases, never versions; adapters re-derive effort per
model. Changelog does not corroborate any prefill change — ledger C3's
prefill pattern rests on non-changelog research.

---

## Part 2 — GitHub Copilot CLI

### Instructions

- v1.0.26 — 2026-04-14 — Duplicate instruction content deduplicated on
  load. Merge-set semantics, not last-wins.
- v1.0.36 — 2026-04-24 — `~/.claude/` custom agents/skills/commands no
  longer auto-loaded. Claude home dir is not a Copilot source.
- v1.0.55 — 2026-05-28 — Recursive discovery; same-name skill precedence.
- v1.0.66 — 2026-06-30 — `@` imports expand in `AGENTS.md`, `CLAUDE.md`,
  and Copilot instruction files.
- v1.0.85 — 2026-09-16 — `copilot instruction list` added. Caveat:
  resolves plugin instructions against global settings only;
  trusted-repo/managed instructions may be active without listing.
  List output is not ground truth for repo scope.
- v1.0.86 — 2026-09-17 — Custom agents opt into repo instructions via
  `include-custom-instructions: true`; adapter must set it explicitly.
- v1.0.89 — 2026-09-28 — `.claude/rules` readable as an instruction
  source. Asymmetric compatibility: Copilot reads some Claude layouts;
  the reverse is not general.
- Current docs (version not stated): supported instruction locations
  include `$HOME/.copilot/muse-instructions.md`,
  `$HOME/.copilot/instructions/**/*.instructions.md`,
  `.github/muse-instructions.md`,
  `.github/instructions/**/*.instructions.md`, `AGENTS.md`, `CLAUDE.md`,
  `GEMINI.md`, `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`. Files combine;
  identical copies deduplicated; no general precedence order defined.
  Ledger C4 (merge, no precedence) confirmed on the docs axis.
- Negative result: no changelog entry for `COPILOT.md`.

Impact: canonical instructions are a merge-set on the Copilot side.
Adapter emits to documented paths only; never rely on enumeration to
prove a file is inactive.

### Skills / custom agents / plugins

- v1.0.17 — 2026-04-03 — Built-in skills introduced (lowest priority).
- v1.0.48 — 2026-05-14 — Skill YAML frontmatter stripped from
  model-injected content; metadata stays out of the prompt body.
- v1.0.55 — 2026-05-28 — Skill precedence: project > plugin-dir >
  personal > custom; first found wins on duplicate names.
- v1.0.62 — 2026-06-13 — Symlinked skills and nested `.github/agents` /
  `.claude/agents` discovery fixed.
- v1.0.66 — 2026-06-30 — Same-named skills from different plugins
  coexist via namespacing.
- v1.0.74 — 2026-07-23 — Open Plugin Spec v1 support; plugin root
  `mcp.json`.
- v1.0.78 — 2026-08-03 — First-party plugin auto-update
  (`COPILOT_AUTO_UPDATE=false` to pin).
- v1.0.83 — 2026-09-04 — Custom-agent ordered model fallbacks and
  required-model policy.
- v1.0.85 — 2026-09-16 — Dedicated `plugin` / `mcp` / `skill` commands;
  cross-kind `plugins` flags removed. Scripts using removed flags break.
- Current docs: skill load order includes `.github/skills/`,
  `.agents/skills/`, `.claude/skills/` (project scope), `~/.copilot/skills/`,
  `~/.agents/skills/`, plugin dirs, `COPILOT_SKILLS_DIRS`, built-in
  (lowest). Note the asymmetry: Copilot consumes `.agents/skills` and
  `.claude/skills`; Claude Code consumes neither `.agents/skills` (Part 1
  negative result). Custom agents: project `.github/agents/` and
  `.claude/agents/` walked cwd→Git root, `.github/agents/` wins at same
  level; `.agent.md` or `.md`; filename = ID.
- Current docs (plugin reference): Agent Plugins 1.0 portable surface is
  `skills/*/SKILL.md` + root `mcp.json` only. Agents, commands, rules,
  hooks, LSP live under `com.github.copilot/` namespaced paths.

Impact: one portable tree does not exist. Adapter emits per-target
native trees; canonical names need namespace mapping on the Copilot
side; plugin packaging is target-specific.

### MCP

- v1.0.21 — 2026-04-07 — `copilot mcp` management command.
- v1.0.22 — 2026-04-09 — `.vscode/mcp.json` source removed; CLI reads
  `.mcp.json` with `mcpServers` key. VS Code layout is not a passthrough.
- v1.0.40 — 2026-05-01 — Prompt-mode workspace MCP behind opt-in env
  gate (`GITHUB_COPILOT_PROMPT_MODE_WORKSPACE_MCP`).
- v1.0.49 — 2026-05-18 — Trusted prompt mode auto-loads workspace MCP.
- v1.0.61 — 2026-06-09 — `.github/mcp.json` workspace auto-loading
  added. Two workspace paths now coexist.
- v1.0.81 — 2026-08-27 — MCP spec 2026-07-28 support.
- v1.0.87 — 2026-09-21 — Built-in servers (`github-mcp-server`,
  `playwright`, `fetch`, `time`) visible in list/get;
  `--disable-builtin-mcps` to turn off.
- Current docs precedence: `--additional-mcp-config` > plugin servers >
  workspace `.mcp.json` / `.github/mcp.json` (trusted folder required;
  same level `.mcp.json` wins) > `~/.copilot/mcp-config.json`. Invalid
  entries skipped with warning; malformed file skipped entirely;
  enterprise allowlist fail-closed.

Impact: project MCP not appearing in unauthenticated `copilot mcp list`
(S4-adjacent observation) is consistent with trust gating, not absence.
Adapter emits Copilot-native MCP files with `mcpServers`; never copies
Claude/VS Code layouts.

### Hooks

- v1.0.15 — 2026-04-01 — `postToolUseFailure` added; `postToolUse`
  becomes success-only. Same event split as Claude (Part 1 §Hooks).
- v1.0.16 — 2026-04-02 — `permissionRequest` added.
- v1.0.21 — 2026-04-07 — PascalCase event names get VS Code-compatible
  snake_case payloads: dual payload dialects keyed by event-name casing.
- v1.0.24 — 2026-04-10 — `preToolUse` honors modified args and
  `additionalContext`. Hooks are mutating middleware, not just gates.
- v1.0.35 — 2026-04-23 — HTTP hooks; permission-granting events require
  HTTPS.
- v1.0.40 — 2026-05-01 — Prompt mode gates repo hooks behind opt-in
  env vars (`GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS`); auto when folder
  trusted or `COPILOT_ALLOW_ALL=true` (exact string).
- v1.0.49 — 2026-05-18 — Repo hooks in `.github/hooks/` load in trusted
  prompt mode; hooks fire for subagent tool calls.
- v1.0.56 — 2026-05-29 — `preToolUse` errors: command hooks fail
  closed, timeouts fail open, HTTP hooks fail open. Choose hook type by
  security requirement.
- v1.0.60 — 2026-06-05 — `/env` shows hook counts and provenance. This is
  the verification surface when docs and runtime disagree.
- v1.0.62 — 2026-06-13 — Claude-format matchers/payload names supported
  as an input dialect (`bash`→`Bash`, `view`→`Read`, etc.). Claude hook
  configs are a supported input, not identical semantics.
- v1.0.67 — 2026-06-30 — Hook timeouts fail open.
- v1.0.81 — 2026-08-27 — Hooks receive `traceparent`/`tracestate`; hook
  execution joins the OTel trace.
- v1.0.85 — 2026-09-16 — `/clear` runs `sessionEnd`.
- Current docs: 15 events (`agentStop`, `errorOccurred`, `notification`,
  `permissionRequest`, `postToolUse`, `postToolUseFailure`, `preCompact`,
  `preToolUse`, `sessionEnd`, `sessionStart`, `subagentStart`,
  `subagentStop`, `userPromptSubmitted`, `userPromptTransformed`, plus
  lifecycle coverage above). Envelope `{ "version": 1, "hooks": { … } }`;
  sources combined: policy, `.github/hooks/*.json`, `~/.copilot/hooks/`,
  inline settings incl. `.claude/settings*.json`, plugins. Output bounded
  at 10 MiB per invocation.

Impact: canonical hooks need a real per-target adapter with per-event
output contracts — not a generic onEvent. Headless runs are
safe-by-default: repo hooks do not run in prompt mode without trust or
explicit opt-in. See ledger flag S4 below before citing our E4 result.

### OpenTelemetry

- Baseline: v1.0.4 — 2026-03-11 — initial OTel instrumentation.
- v1.0.20 — 2026-04-07 — `copilot help monitoring` added.
- v1.0.45 — 2026-05-11 — MCP calls emit standard `tool_call` spans.
- v1.0.61 — 2026-06-09 — HTTP/protobuf OTLP via standard OTel env vars.
- v1.0.64 — 2026-06-23 — Compaction and cache/reasoning accounting
  queryable (`gen_ai.conversation.compacted`, cache token fields).
- Current docs: OTel off by default, zero overhead. Activates on
  `COPILOT_OTEL_ENABLED=true`, `OTEL_EXPORTER_OTLP_ENDPOINT` set, or
  `COPILOT_OTEL_FILE_EXPORTER_PATH` set (alone selects the file
  exporter). Content capture off by default;
  `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` adds
  `gen_ai.input.messages`, `gen_ai.output.messages`,
  `gen_ai.system_instructions`, `gen_ai.tool.definitions`, tool
  arguments/results. Spans: `invoke_agent` root, `chat`, `execute_tool`;
  lifecycle events include hook start/end/error, skill invocation,
  compaction; metrics include MCP connection counts. Provider recorded
  as `gen_ai.provider.name`. The capture is a GenAI
  semantic-convention representation, not the literal HTTP wire body
  (docs define it as span attributes; no raw-body mode is documented).

Impact: OTel is the dependable cross-harness observability bridge —
file JSONL needs no collector and works regardless of hook-loader
health. Normalizer target: `gen_ai.*` on both sides. Claude's
`OTEL_LOG_RAW_API_BODIES=file:` is the one true raw-body source; do not
claim byte parity for Copilot.

### BYOK

- 2026-04-07 (GitHub Changelog) — BYOK + local models announced: Azure
  OpenAI, Anthropic, OpenAI-compatible, Ollama/vLLM/Foundry Local.
  `COPILOT_OFFLINE=true`; no silent GitHub fallback. Built-in subagents
  inherit provider settings.
- v1.0.22 — 2026-04-09 — Anthropic BYOK permission/hooks fixed.
- v1.0.66 — 2026-06-30 — Anthropic adaptive-thinking mismatch fixed.
- 2026-06-17 — Enterprise BYOK: admin-configured external models in
  `/model`.
- Current docs: two config generations. Legacy env vars
  (`COPILOT_PROVIDER_TYPE/BASE_URL/API_KEY/MODEL_ID`, `COPILOT_MODEL`)
  plus newer `providers.json` (`COPILOT_PROVIDERS_CONFIG`), which takes
  precedence when it declares any provider/model.
  `COPILOT_PROVIDER_API_KEY_COMMAND` (fresh key per request) takes
  precedence over the static key.

Impact: ledger S7 (one Anthropic key drives both harnesses) is
supported by the announced feature. New adapter work should emit
`providers.json`; env vars are the legacy form. `COPILOT_MODEL` is
required alongside the provider vars.

### Rubber duck

- v1.0.18 — 2026-04-04 — Experimental "Critic" for Claude sessions
  (complementary model).
- v1.0.42 — 2026-05-06 — GPT sessions gain Claude-powered duck;
  pairing bidirectional (2026-05-07 Changelog).
- v1.0.49 — 2026-05-18 — `/rubber-duck` experimental command.
- v1.0.56 — 2026-05-29 — `builtInAgents.rubberDuck` setting.
- v1.0.58 — 2026-06-02 — Enabled by default; GA (2026-06-02 Changelog).
- v1.0.60 — 2026-06-05 — `builtInAgents.rubberDuckAutoInvoke` exists;
  auto-invocation is a separate, opt-in setting.
- v1.0.87 — 2026-09-21 — Enabled for every model family and low-cost
  tiers.
- Current docs: built-in, read-only critic; reviews plans/design/
  implementation/tests; no file edits; main agent decides.

Impact: grounds ledger C2. Treat as a native Copilot subagent, never a
canonical agent definition.

### Logging

- v1.0.52 — 2026-05-23 — Resumed-session relative `--log-dir` resolves
  against saved cwd; old logs under `~/.copilot/logs/` pruned at startup.
- Negative result: no changelog entry for the introduction of
  `--log-level` or `--log-dir`. Current reference documents both:
  `--log-dir=DIRECTORY` (default `~/.copilot/logs/`),
  `--log-level=LEVEL` (`none|error|warning|info|debug|all|default`).

Impact: logging is a launch-time contract. Canonical run wrappers set
level/dir explicitly; never rely on defaults.

### Cross-cutting (Copilot)

- Prompt-mode trust gates recur across hooks, MCP, and extensions:
  repo-controlled code does not run headless without trust or opt-in.
  This is the single most important headless-behavior rule for the
  adapter.
- `COPILOT_ALLOW_ALL=true` (exact string) also trusts the working
  directory; other truthy spellings only auto-approve tools.
- `/env` is the in-product inventory (instructions, MCP, skills, agents,
  hooks, plugins). When docs and runtime disagree, `/env` counts are
  the first check.
- No v1.0.84 heading exists in the changelog. Version sequence is not
  contiguous; never assume a missing version exists.

---

## Part 3 — Claims-ledger cross-checks (2026-09-30)

No ledger verdict is overturned by this audit. Flags below are
refinements, postdating evidence, or open re-tests — not verdict edits.

| Claim | Flag | Disposition |
|---|---|---|
| C1 (`/advisor`) | UPGRADED EVIDENCE. Official advisor docs + v2.1.260 (2026-09-03) text form ground the claim. New constraints: Anthropic API only; requires feature-flag fetching (telemetry/flag-disabled sessions keep it off); subagents re-validate pairing. | Verdict stands (PROVEN). Note the telemetry-disabled interaction in tips-claude before recommending `/advisor` beside OTel-hardened profiles. |
| C2 (rubber duck) | NUANCE. Enabled by default (v1.0.58, GA 2026-06-02) but auto-invoke is a separate opt-in setting (v1.0.60, `rubberDuckAutoInvoke`, default off). Prior phrasing "auto-consulted on non-trivial work" is stronger than the changelog supports. | Verdict stands (PROVEN feature). Re-word the evidence note: default-on availability, opt-in auto-invoke, until a live check pins behavior. |
| C3 (Opus 5.5 prompt regression) | CONSISTENT. Changelog contains no "prefill" entry and no general regression claim; it does document per-model effort defaults (v2.1.251) and `/doctor prompt-audit` (v2.1.283). General claim stays UNVERIFIABLE; the prefill pattern rests on non-changelog research (opus-55-prompt-claim.md). | No change. |
| C4 (instruction discovery) | POSTDATED EVIDENCE. v2.1.281 (2026-09-23) lifted the v2.1.277 provider restriction on AGENTS.md (Bedrock/Vertex/Foundry/gateways/telemetry-disabled). The restriction is quoted in the underlying research brief (`hidden_files/research/instructions-files.md`) and is now historical; the wiki note never carried it, so no note edit needed. Copilot side confirmed: merge, no precedence; BUT changelog shows no `.github/muse-instructions.md` entry while docs list the path — same docs/runtime drift pattern as S4. | Verdict stands (PROVEN). |
| S1 (one install, both tools) | SUPPORTED, asymmetry noted. Copilot consumes `.agents/skills`, `.claude/skills`, `.claude/agents`, `.claude/rules`; Claude Code consumes none of the `.agents/*` paths. Install parity today works because adapters emit per-target native trees, not because layouts are shared. | No change. Keep adapters explicit. |
| S4 (failure-capture hook) | ⚠ RE-TEST REQUIRED. Our REFUTED rests on "binary contains no hook loader" (0/5, no loader strings). Changelog contradicts the loader theory: `postToolUseFailure` exists since v1.0.15 (2026-04-01), repo hooks load since v1.0.49 (2026-05-18) — but prompt mode gates repo hooks behind trust / `GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS` (v1.0.40). E4 ran headless; the trust gate predicts exactly 0/5 without any missing loader. The 0/5 observation stands; the mechanism attribution does not. | Verdict stays PARTIAL / Copilot REFUTED *as tested*. Before the deck cites it: re-run E4's Copilot half with trusted folder or `GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS=1`, and check `/env` hook counts (v1.0.60) on the same build. If hooks then fire, S4's Copilot leg flips and the adapter gains the documented envelope only. |
| S7 (one credential, both harnesses) | SUPPORTED, one modernization note. BYOK announced 2026-04-07; our live probe (2026-09-30) used legacy `COPILOT_PROVIDER_*` env vars. Newer `providers.json` (`COPILOT_PROVIDERS_CONFIG`) takes precedence when present; `COPILOT_MODEL` is required. | Verdict stands (PROVEN). Adapter backlog: emit `providers.json`. |
| Models in deck/tips | CURRENT. Sonnet 5.5 default v2.1.284 (2026-09-28), Opus 5.5 default v2.1.280 (2026-09-22), both 1M context with published per-Mtok prices. No Haiku 5.5 in Claude Code through v2.1.285. | Deck may cite defaults as of 2026-09-29. Pin family aliases, not versions. |

Child-lane ⚠ items not carried into the ledger: "Opus 5 in v2.1.219 not
v2.1.220" (lane-local cross-check; no ledger claim cites v2.1.220 — no
action). Both lanes' ⚠ CHECK S4 items are the same finding, merged
above.

---

## Highest-impact changes — summary

The window's story is asymmetric convergence plus governance moving
up-scope. Copilot CLI absorbed the Claude-adjacent surfaces
(`AGENTS.md`, `.claude/skills`, `.claude/agents`, `.claude/rules`, a
15-event hook system with Claude-format input dialect, Open Plugin Spec
portability for skills+MCP only) while keeping its own precedence,
namespacing, and trust gates; Claude Code added native `AGENTS.md`
fallback (v2.1.277, all providers by v2.1.281) but no shared skill path,
and pushed telemetry, raw-body capture, and credential policy into
user/managed scope where project settings can no longer reach
(v2.1.217, v2.1.251). For the bridge, three consequences dominate: (1)
hooks on both sides now split `postToolUse` vs `postToolUseFailure` and
need per-event contracts, but Copilot's prompt-mode trust gate — not a
missing loader — is the live hypothesis behind our E4 0/5, so S4's
Copilot leg needs one trusted-mode re-run before the presentation cites
it; (2) OTel with `gen_ai.*` conventions is the one observability plane
both tools genuinely share (Copilot file JSONL with content capture;
Claude `OTEL_LOG_RAW_API_BODIES=file:` as the only true raw-body
source), making it the right substrate for explaining harness overhead
like the 14.5k-token BYOK gap; (3) model defaults rotated three times
in a quarter (Opus 5 → Opus 5.5 → Sonnet 5.5) with per-model effort
semantics, so canonical configs must pin family aliases and let
adapters re-derive everything else. Canonical content stays
provider-neutral; every shared behavior we claim must still be earned
per target, per build, by eval.


---
RESOLVED 2026-09-30 ~01:45 ET: the S4 re-test above was run. Hooks fire on
v1.0.89 under `COPILOT_ALLOW_ALL=true` (directory trust); untrusted
headless reproduces 0/5. `postToolUseFailure` never fires for shell
failures (tool reports `resultType: success`; exit code in result text).
Full record: `evals/results/2026-09-30-E4.md` addendum.
