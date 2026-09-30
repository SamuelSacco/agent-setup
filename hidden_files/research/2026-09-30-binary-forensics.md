# Binary forensics — Copilot CLI 1.0.89 vs Claude Code 2.1.285

Scope: read-only inspection of installed binaries and local session logs. No CLI sessions run, no API tokens spent. Purpose: explain why a one-word probe ("Reply with exactly: OK") cost ~14.5k input tokens via Copilot BYOK vs ~1.9k via lean Claude Code.

## Install layout

| | Copilot CLI | Claude Code |
|---|---|---|
| Package | `@github/copilot` 1.0.89 | `@anthropic-ai/claude-code` 2.1.285 |
| Entry | `~/workspace/tools/bin/copilot` → `npm-loader.js` → native binary | `~/workspace/tools/bin/claude` → `bin/claude.exe` |
| Native binary | `@github/copilot-linux-x64/copilot`, 174,066,496 B (Node SEA, stripped ELF) | `claude.exe`, ~230 MB (Bun-compiled ELF) |
| JS payload | Extracted at runtime to `~/.cache/copilot/pkg/linux-x64/1.0.89/`; main bundle `app.js` = 7,515,253 B, plus `index.js`, `copilot-sdk/` (index.js 553 KB + extension.js 548 KB, duplicated SDK), `definitions/` (7 built-in agent YAMLs), `schemas/` (2.0 MB api.schema.json + session-events.schema.json), tree-sitter WASMs, prebuilds 116 MB | Single binary; `sdk-tools.d.ts` (169 KB) ships alongside |

All greps below ran against the extracted `app.js` unless noted. The 174 MB native wrapper contains none of the searched strings (payload lives in the cache dir).

## OTel / telemetry env vars in app.js

| String | Hits | Note |
|---|---|---|
| `COPILOT_OTEL_FILE_EXPORTER_PATH` | 7 | Present |
| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` | 4 (as `CAPTURE_MESSAGE_CONTENT` suffix matches) | Present |
| `COPILOT_OTEL_ENABLED` | 4 | Present |
| `COPILOT_OTEL_EXPORTER_TYPE` | 3 | Present |
| `OTEL_LOG_RAW_API_BODIES` | 0 | Claude-side var; absent here as expected |

`copilot help monitoring` runs without auth (exit 0) and documents exactly this surface: activation via `COPILOT_OTEL_ENABLED=true`, `OTEL_EXPORTER_OTLP_ENDPOINT`, or `COPILOT_OTEL_FILE_EXPORTER_PATH`; content capture via `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` adds "full prompt and response messages, system instructions and tool definitions, tool call arguments and results." Metrics exported are `gen_ai.client.*` / `gen_ai.invoke_agent.*` / `gen_ai.execute_tool.*` (all present in app.js). No `gen_ai.input.messages` / `gen_ai.system_instructions` attribute literals exist in app.js (0 hits) — content capture is documented semantically in help, not visible as attribute-name literals in the bundle; the fields likely materialize in native/runtime code. Verdict on Samuel's claim: CONFIRMED for the env vars, exporter behavior, and help topic; the exact `gen_ai.*` content attribute names are UNVERIFIED locally.

`OTEL_LOG_RAW_API_BODIES` in Claude's binary: 6 hits, alongside `CLAUDE_CODE_ENABLE_TELEMETRY` (17), `apiKeyHelper` (114). The Bun string table is too mangled to confirm the `file:<dir>` semantics from strings; that part stays documentation-sourced, not locally proven.

## BYOK provider vars in app.js

All present: `COPILOT_PROVIDER_BASE_URL` (14), `COPILOT_PROVIDER_API_KEY` (9), `COPILOT_PROVIDER_TYPE` (5), `COPILOT_PROVIDER_MODEL_ID` (5), plus `_WIRE_MODEL`, `_HEADERS`, `_GHES_HOST`, `_API_KEY_COMMAND`, `_WIRE_API`, `_TRANSPORT`, `_MAX_PROMPT_TOKENS`, `_MAX_OUTPUT_TOKENS`, `_BEARER_TOKEN`, `_AZURE_API_VERSION`. `COPILOT_ENABLE_ALT_PROVIDERS` (9) also exists.

## Hook surface

Event-name literals in app.js: `postToolUseFailure` 0, `userPromptSubmitted` 0, `agentStop` 0, `preToolUse` 0, `postToolUse` 0 (case variants also 0; `sessionStart` ×14 and `SessionStart` ×10 are session-lifecycle methods, not hook events; `postToolUseInputJson` is a session-store field).

Hook machinery IS present, three layers:

1. Config docs embedded in app.js: `disableAllHooks`, `hooks` key "keyed by event name (same schema as .github/hooks/*.json)" in global config.json / repo settings.json; settings UI has a Hooks resource (`hooks.**`, `disabledHooks`, `disableAllHooks` globs).
2. Loader: `getHooksDir()` resolves `<gitroot>/.github/hooks`; `S.hookSessionCreate({cwd, repoRoot, sessionId, settingsJson, userHooksDir: <COPILOT_HOME>/hooks, ...})` delegates execution to the native host API (`S.*`), so event-name strings never appear in JS.
3. SDK/extension API: `copilot-sdk/types.d.ts` defines full handler types (`PreToolUseHandler`, `PostToolUseHandler`, `PostToolUseFailureHandler`, `UserPromptSubmittedHandler`, `SessionStartHandler`, …) and `copilot-sdk/{index,extension}.js` wire `postToolUseFailure: this.hooks.onPostToolUseFailure`. Extensions register hooks programmatically over JSON-RPC.

Behavioral check: all 8 local session logs (`~/.copilot/session-state/*/events.jsonl`) contain zero `hook.start`/`hook.end`/`hook.progress` events. The runtime emits those event types per `schemas/session-events.schema.json`, so a fired hook would have left a trace. None did — including sessions run with repo hook files present (E4). Consistent with the earlier E4 REFUTED verdict for repo-file command hooks in this build, while leaving the extension-API path genuinely untested. Possible confound: hook sessions are created natively at session start; if the native host failed to parse our hook JSON it may have silently created an empty hook set. Not determinable from the bundle.

## Tool surface size

Tool schemas are not statically present in app.js, the SDK JS, or the native binary (0 hits for `inputSchema` outside 7 incidental matches; 0 inline `{"type":"object","properties":…}` literals; no tool description text). Definitions are generated/assembled host-side at runtime, so serialized size cannot be summed from the bundle. Catalog size from `definitions/*.agent.yaml`:

- Local tools referenced: bash, powershell, read_bash, read_powershell, stop_bash, stop_powershell, view, glob, grep, lsp, context_board (11), plus create/str_replace/insert/apply_patch, task/sub-agent tools, web_search, web_fetch, sql, ask_user visible in app.js code paths. Main agent runs `tools: ["*"]` (full catalog).
- GitHub MCP tools referenced: 19 (`github-mcp-server/*`), read-only subset in explorer agents; the main agent's connected set is larger when the GitHub MCP server is attached.

Estimate by subtraction from the measured BYOK session (below): 14.5k input − ~6.2k system − ~0.1k user/context ≈ **~8k tokens of tool definitions** for ~30+ advertised tools. Plausible: several tools (bash, lsp, sql, task) carry schemas well over 500 tokens each.

Claude side: full tool catalog is not in `sdk-tools.d.ts` as a countable list (types only). Size evidence comes from transcripts instead (below).

## System prompt size — measured, not estimated

Copilot records its assembled system prompt verbatim as a `system.message` event in each session log. Two real sessions:

- BYOK probe (cwd `/tmp`, model `claude-haiku-4-5-20251001`, 2026-09-30T05:06Z): **23,209 chars** ≈ 5.8–6.4k tokens. Sections: identity+autonomy preamble 358, Tone and style 224 (heading split understates), Search and delegation, Tool usage efficiency **16,805 chars** (includes the task-completion contract), Security review caller contract **5,522 chars**. No AGENTS.md (cwd had none).
- GitHub-hosted probe (cwd `/home/hatch`): 33,337 chars — includes the repo's full AGENTS.md injected under a `# AGENTS.md` heading (+~10k chars ≈ +2.8k tokens). Every other local session: ~80 KB system.message JSON (content ~33k chars, same reason).

The user message is also wrapped: `transformedContent` prepends `<current_datetime>…</current_datetime>`. Small but nonzero.

Claude Code comparison from local transcripts (`~/.claude/projects/`):

- `--bare` probe (`-tmp-claude-bare-test`, Haiku): **1,867 input tokens total**, 0 cache tokens. That is the entire request — system, tools, user.
- Full-harness run (`-tmp-e1-claude`): first call already 8,575 cache-creation + 13,897 cache-read tokens. Full Claude is also a ~10k+-token harness; the 1.9k figure is bare mode only.

## Where the 14.5k went (Copilot BYOK probe)

| Component | Tokens (est.) | Evidence |
|---|---|---|
| System prompt | ~6.2k | 23,209 chars in session log, measured |
| Tool definitions | ~8k | Subtraction; 30+ tools, schemas host-generated |
| User message + datetime wrapper + framing | ~0.2k | Session log |
| **Total** | **~14.5k** | CLI footer |

## Summary

The 14.5k vs 1.9k gap is harness constant overhead, measured piece by piece: Copilot's assembled system prompt alone is 23,209 chars (~6.2k tokens — 3.3× the *entire* bare Claude request), dominated by a 16.8k-char tool-usage/task-completion contract and a 5.5k-char security-review contract, and the remaining ~8k is the always-on tool catalog (30+ built-in and GitHub MCP tool schemas, generated host-side and shipped with every request). The "lean" Claude number is `--bare` mode (1,867 tokens all-in), which strips exactly the layers Copilot always sends; run full-harness, Claude's first call is comparably heavy (8.6k cache-create + 13.9k cache-read). So the honest framing is not "Copilot's harness is bloated" but "the comparison was full harness vs bare harness" — and Copilot, unlike Claude, has no bare mode, plus it silently injects repo AGENTS.md (~+10k chars) whenever the cwd has one.
