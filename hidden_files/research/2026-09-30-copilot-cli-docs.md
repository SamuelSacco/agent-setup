# Copilot CLI docs verification — 2026-09-30

Source: docs.github.com only. Verdicts cover what the documentation says;
binary behavior is a separate axis (local v1.0.89 results noted where relevant).

## 1. First-class OTel support; `copilot help monitoring`
**PROVEN.** CLI command reference documents OTel export and lists `monitoring`
as a help topic.

> "Copilot CLI can export traces and metrics via OpenTelemetry (OTel), giving you visibility into agent interactions, LLM calls, tool executions, and token usage. All signal names and attributes follow the OTel GenAI Semantic Conventions."

> "| `copilot help [TOPIC]` | Display help information. Help topics include: `billing`, `config`, `commands`, `environment`, `logging`, `monitoring`, `permissions`, `providers`, and `sandbox`. |"

URL: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference

## 2. `COPILOT_OTEL_FILE_EXPORTER_PATH` alone enables OTel + file exporter
**PROVEN.** Path alone both enables OTel and auto-selects the file exporter.
`COPILOT_OTEL_ENABLED` and `COPILOT_OTEL_EXPORTER_TYPE` are documented.

> "OTel is off by default with zero overhead. It activates when any of the following conditions are met: `COPILOT_OTEL_ENABLED=true` / `OTEL_EXPORTER_OTLP_ENDPOINT` is set / `COPILOT_OTEL_FILE_EXPORTER_PATH` is set"

> "| `COPILOT_OTEL_FILE_EXPORTER_PATH` | — | Write all signals to this file as JSON-lines. Setting this automatically enables OTel. |"

> "| `COPILOT_OTEL_EXPORTER_TYPE` | `otlp-http` | Exporter type: `otlp-http` or `file`. Auto-selects `file` when `COPILOT_OTEL_FILE_EXPORTER_PATH` is set. |"

## 3. `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`
**PROVEN.** Default is `false`; only metadata is captured unless set.

> "| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` | `false` | Capture full prompt and response content. See Content capture. |"

> "By default, no prompt content, responses, or tool arguments are captured—only metadata like model names, token counts, and durations. To capture full content, set `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`."

Privacy warning, verbatim:

> "Content capture may include sensitive information such as code, file contents, and user prompts. Only enable this in trusted environments."

## 4. Captured fields; provider as `gen_ai.provider.name`
**PROVEN.** All six fields documented verbatim in the content-capture table.

> "| `gen_ai.input.messages` | Full prompt messages (JSON) |"
> "| `gen_ai.output.messages` | Full response messages (JSON) |"
> "| `gen_ai.system_instructions` | System prompt content (JSON) |"
> "| `gen_ai.tool.definitions` | Tool schemas (JSON) |"
> "| `gen_ai.tool.call.arguments` | Tool input arguments |"
> "| `gen_ai.tool.call.result` | Tool output |"
> "| `gen_ai.provider.name` | Provider (for example, `github`, `anthropic`) | Both |"

Signal shape: spans (`invoke_agent` root, `chat` / `execute_tool` children),
traces + metrics; no exported OTel logs signal in the CLI reference.

## 5. OTel capture is NOT the literal HTTP wire body
**PROVEN in substance.** Docs define the capture entirely as semantic-convention
span attributes; no sentence describes a raw request/response body dump. The
only HTTP wire protocol mentioned is the telemetry exporter's own OTLP
transport. No explicit "this is not the wire body" sentence exists — the proof
is the positive definition of what is captured.

## 6. `--log-level all --log-dir <dir>`
**PROVEN.** Reference table uses `--flag=VALUE` form.

> "| `--log-level=LEVEL` | Set the log level (choices: `none`, `error`, `warning`, `info`, `debug`, `all`, `default`). |"
> "| `--log-dir=DIRECTORY` | Set the log file directory (default: `~/.copilot/logs/`). |"

## 7. Hooks
**PROVEN as documented; minimum CLI version UNVERIFIABLE.** Docs describe
hooks as a shipped Copilot CLI feature with no preview banner and no stated
minimum CLI version — only the config schema version (`1`).

Locations:

> "You define hooks in JSON files, stored in your repository at `.github/hooks/*.json`. ... Copilot CLI also supports personal hooks that you store in your home directory at `~/.copilot/hooks/*.json`."

> "**Repository-level hook files** — `.github/hooks/*.json` in the repository root."
> "**User-level hook files** — `*.json` files in the user-level hooks directory. By default this is `~/.copilot/hooks/` on macOS and Linux... If `COPILOT_HOME` is set, it is `$COPILOT_HOME/hooks/`."

Schema:

> "You configure hooks using a special JSON format. The JSON must contain a `version` field with a value of `1` and a `hooks` object containing arrays of hook definitions."
> "`bash` | string | One of `bash`, `powershell`, or `command`, unless `exec` is specified | Shell command for Unix."
> "`timeoutSec` | number | No | Timeout in seconds. Default: `30`."

Events: the hooks reference lists 14 (`agentStop`, `errorOccurred`,
`notification`, `permissionRequest`, `postToolUse`, `postToolUseFailure`,
`preCompact`, `preToolUse`, `sessionEnd`, `sessionStart`, `subagentStart`,
`subagentStop`, `userPromptSubmitted`, `userPromptTransformed`). Note:
`postToolUseFailure` appears only in the full reference table, not in the
CLI how-to's 6-key template.

> "`postToolUseFailure` | After a tool completes with a failure. | Yes — can provide recovery guidance via `additionalContext` (exit code `2` for command hooks). | Fires."

Loading:

> "Hooks are loaded from the following sources in order (policy, then user, then project, then plugins) and combined. When the same event appears in multiple sources, all hook entries from all sources are run."
> "Changes to hook configurations are loaded when the CLI starts."

Surfaces: one format shared by Copilot CLI and Copilot cloud agent, with
"CLI only" / "Cloud agent only" callouts. VS Code appears only as a
PascalCase-compatible payload format, not a third hooks surface.

URLs:
- https://docs.github.com/en/copilot/concepts/agents/hooks
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-hooks
- https://docs.github.com/en/copilot/reference/hooks-reference
- https://docs.github.com/en/copilot/tutorials/copilot-cli-hooks

**Local discrepancy (not a docs question):** installed v1.0.89 did not
execute repo hooks (0/5, no hook-loader strings in bundle). Docs state no
version gate, so docs alone cannot explain it. Open hypotheses: build newer
than docs snapshot mismatch, feature flag, or org policy gating. Docs do
note CLI availability requires org Copilot policy where applicable:

> "GitHub Copilot CLI is available with all Copilot plans. If you receive Copilot from an organization, the Copilot CLI policy must be enabled in the organization's settings."

## 8. Instruction-file loading
**PROVEN** for `AGENTS.md` and `.github/muse-instructions.md`; **REFUTED**
for `COPILOT.md` (absent from the documented list).

> "Custom instructions are persistent guidance that the Copilot CLI loads from instruction files at the start of a session."

Documented locations: `$HOME/.copilot/muse-instructions.md`,
`$HOME/.copilot/instructions/**/*.instructions.md`,
`.github/muse-instructions.md`, `.github/instructions/**/*.instructions.md`,
`AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, `GEMINI.md`,
`.claude/rules/**/*.md`, plus dirs in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`.
`COPILOT_HOME` replaces `$HOME/.copilot`.

> "Unless noted in the table below, Copilot CLI discovers repository and agent instruction files in the standard locations: the repository root, the current working directory, intermediate directories between them, and any directories nested in the path of a file it is working on."

Precedence — **PROVEN: no general precedence order; files are merged.**

> "When multiple applicable user-level and repository instruction files exist, Copilot CLI combines their instructions. It removes duplicate copies of identical user-level `copilot-instructions.md`, repository-wide, and agent instructions, but does not define a general precedence order between these files. Avoid conflicting instructions."

> "Copilot CLI loads custom instructions from these locations simultaneously (all are merged):"

URLs:
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference

## 9. BYOK env vars
**PROVEN.** All four documented; `COPILOT_MODEL` additionally required.

> "You can configure Copilot CLI to use your own LLM provider, also called BYOK (Bring Your Own Key), instead of GitHub-hosted models. This lets you connect to OpenAI-compatible endpoints, Azure OpenAI, or Anthropic, including locally running models such as Ollama."

- `COPILOT_PROVIDER_BASE_URL` (required): "The base URL of your model provider's API endpoint."
- `COPILOT_PROVIDER_TYPE`: "The provider type: `openai` (default), `azure`, or `anthropic`."
- `COPILOT_PROVIDER_API_KEY`: "Your API key for the provider. Not required for providers that do not use authentication, such as a local Ollama instance."
- `COPILOT_PROVIDER_MODEL_ID`: "The well-known model name used to identify model capabilities and token limits."
- `COPILOT_MODEL` (required): "The model identifier to use. You can also set this with the `--model` command-line flag."

Also documented: `COPILOT_PROVIDERS_CONFIG` → `providers.json` registry,
which takes precedence over the legacy `COPILOT_PROVIDER_*` vars when it
declares any provider or model.

URL: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-byok-models

## Summary

Every Copilot CLI claim Samuel relayed checks out against official GitHub docs: OTel is first-class with `copilot help monitoring`; setting `COPILOT_OTEL_FILE_EXPORTER_PATH` alone enables OTel and selects the file exporter; `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` captures full `gen_ai.*` message/system/tool content with `gen_ai.provider.name` — a semantic-convention span representation, not a raw HTTP wire body (proven by the docs' positive definition, not an explicit disclaimer); `--log-level all` and `--log-dir` are documented; hooks are documented as a shipped feature (`.github/hooks/*.json`, schema `version: 1`, 14 events including `postToolUseFailure`) with no preview marker and no minimum CLI version, so the local v1.0.89 no-execution result remains an unexplained binary-vs-docs gap — docs are PROVEN, version gating UNVERIFIABLE. Instruction files merge with no documented precedence (PROVEN); `COPILOT.md` is REFUTED as a documented CLI instruction file; all four BYOK env vars are PROVEN, with `COPILOT_MODEL` also required and a `providers.json` registry that overrides the env vars.
