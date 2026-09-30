# OTel instrumentation + harness overhead decomposition — 2026-09-30 (~01:24 ET)

Question from Samuel: Copilot's harness spent ~14.5k input tokens on a
one-word reply vs ~1.9k for lean Claude Code. Why? And do both CLIs expose
real capture (raw API bodies / OTel content) to explain it from data?

Method: identical probe (`Reply with exactly: OK`), identical model
(`claude-haiku-4-5-20251001`), identical Anthropic key, both harnesses
instrumented. Artifacts: `~/agent-logs/claude/raw/`, `~/agent-logs/copilot/otel.jsonl`.

## Claude Code — raw API-body capture

`CLAUDE_CODE_ENABLE_TELEMETRY=1 OTEL_LOGS_EXPORTER=console
OTEL_LOG_RAW_API_BODIES=file:~/agent-logs/claude/raw` + `--bare` +
apiKeyHelper. Wrote:

- `<uuid>.request.json` (5,417 B), `<request-id>.response.json`, `index.jsonl`

Verdict: **PROVEN.** The `file:<dir>` mode exists and behaves as described,
including the index file.

Captured request body, decomposed (chars ≈ tokens×4):

| Part | Size |
|---|---|
| system (3 blocks) | 463 chars |
| tools | 3 defs — Bash, Edit, Read — 3,488 chars |
| messages | 848 chars |
| API-reported input tokens | **1,866** (cost $0.002191, run 1) |

`--bare` is the lean configuration; this is the run behind the "~1.9k" figure.
"Lean mode" is not a product feature — it is this flag.

## Claude Code — default mode (no `--bare`), same probe

| Part | Size |
|---|---|
| system | 28,493 chars |
| tools | 12 defs (Agent, Bash, Edit, ListAgents, Read, ReportFindings, ScheduleWakeup, Skill, ToolSearch, Workflow, DeferredToolPlaceholder, Write) — 44,365 chars |
| total input context | **20,589 tokens** (10 fresh + 6,682 cache-create + 13,897 cache-read), $0.0099472 |

## Copilot CLI — OTel content capture

`COPILOT_OTEL_FILE_EXPORTER_PATH` alone auto-enabled OTel (file exporter);
`OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` added full content.
16 JSONL records (2 spans + metrics). `gen_ai.provider.name=anthropic`,
`server.address=api.anthropic.com` — the BYOK path is visible in the trace.

Verdict: **PROVEN.** First-class OTel with file exporter and optional full
message-content capture exists in v1.0.89. It is Copilot's OTel GenAI
representation, not the literal provider HTTP body — for normalization that
is the better input anyway.

`copilot help monitoring` ships the full reference locally (saved:
`hidden_files/research/copilot-help-monitoring.txt`).

## Why 14.5k: the decomposition

Span `chat claude-haiku-4-5-20251001`, run 1:

| Part | Size |
|---|---|
| `gen_ai.system_instructions` | 23,655 chars (1 block) |
| `gen_ai.tool.definitions` | 30,900 chars — **23 tools** |
| `gen_ai.input.messages` | 148 chars (prompt wrapped with injected `<current_datetime>`) |
| API-reported input tokens | **14,510** |

Largest tool schemas: `session_store_sql` 6,701 chars; `task` 3,303; `bash`
2,840. Five of the 23 tools come from an auto-connected `github-mcp-server`;
two skills were loaded (`customize-cloud-agent`, `github-pr-media`). The user
prompt is ~38 tokens of the 14,510. The rest is fixed harness surface paid
before the first user token.

Cache behavior, run 2 (fresh session, identical prompt): input 14,509 with
cache_read 9,547 + cache_write 4,952. ~66% of the prefix is byte-stable
across sessions and cache-read at the lower rate; the remainder is rebuilt
per session.

## Verdict on the gap

**Explained, not anomalous — and the naive ratio is wrong.** Both harnesses
pay system-prompt + tool-schema before the user speaks. The real numbers:

| Configuration | Input context for "OK" |
|---|---|
| Claude Code `--bare` | 1,866 |
| Copilot CLI default (BYOK) | 14,510 |
| Claude Code default | 20,589 (mostly cache-read after warm-up) |

Copilot's surface (23 tools + MCP + skills + ~5.9k-token system prompt) is
~7× Claude `--bare`'s, but Claude's *default* surface is larger than
Copilot's. The overnight-briefing line "Copilot wastes 14.5k" does not
survive this measurement; the defensible claim is that `--bare` shows how
much of either harness's cost is fixed surface, and both tools let you see
it exactly (raw bodies / OTel content). Quote configurations, never a
single ratio.
