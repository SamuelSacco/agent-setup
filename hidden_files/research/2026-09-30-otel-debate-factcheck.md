# OTel essay — fact-check brief (debate: FACT-CHECKER)

Date: 2026-09-30 (~01:35 ET). Read-only: no CLIs run, no API spend, no commits.
Scope: Claude Code v2.1.285, Copilot CLI v1.0.89 (local builds); official docs
as of tonight. Sources: Anthropic monitoring docs, GitHub Copilot CLI docs and
the installed binary's own `copilot help monitoring`, plus tonight's local
captures (`~/agent-logs/claude/raw*/`, `~/agent-logs/copilot/otel.jsonl`).

Verdicts: **PROVEN** / **REFUTED** / **UNVERIFIABLE**.

---

## 1. Claude span hierarchy + beta flag

**PROVEN.** Anthropic's monitoring page has a section titled "Traces (beta)"
and states tracing is off by default, enabled by setting both
`CLAUDE_CODE_ENABLE_TELEMETRY=1` and `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`
(`ENABLE_ENHANCED_TELEMETRY_BETA` also accepted), then `OTEL_TRACES_EXPORTER`.

All five span names exist exactly as the essay gives them:

- `claude_code.interaction` — "Each user prompt starts a `claude_code.interaction`
  root span. API calls, tool calls, and hook executions are recorded as its children."
- `claude_code.llm_request` — full attribute table (model, TTFT, tokens, retries,
  request IDs, stop reasons).
- `claude_code.tool` — tool call span; subagent API/tool spans nest under it.
- `claude_code.tool.blocked_on_user` — "one for the time spent waiting on a
  permission decision."
- `claude_code.tool.execution` — "one for the execution itself."

Source: https://code.claude.com/docs/en/monitoring-usage (traces section).

Two precisions the essay omits: (a) there is also a `claude_code.hook` span, but
it appears **only under detailed beta tracing** (`ENABLE_BETA_TRACING_DETAILED=1`
plus `BETA_TRACING_ENDPOINT`, org allowlist for interactive CLI) —
`CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` alone does not produce it; (b) not locally
exercised — tonight's Claude runs used logs + raw bodies, never the traces
exporter, so the hierarchy is doc-proven, not capture-proven.

## 2. Content flags `OTEL_LOG_USER_PROMPTS` / `OTEL_LOG_ASSISTANT_RESPONSES` / `OTEL_LOG_TOOL_DETAILS` / `OTEL_LOG_TOOL_CONTENT`

**PROVEN.** All four exist with exactly those names on the same docs page:

- `OTEL_LOG_USER_PROMPTS` — "Enable logging of user prompt content (default: disabled)"
- `OTEL_LOG_ASSISTANT_RESPONSES` — "Enable logging of assistant response text on
  `assistant_response` events... When unset, falls back to the value of
  `OTEL_LOG_USER_PROMPTS`. Requires Claude Code v2.1.193 or later"
- `OTEL_LOG_TOOL_DETAILS` — "Enable logging of tool parameters and input arguments
  in tool events and trace span attributes: Bash commands, MCP server and tool
  names, skill names... and tool input" (also un-redacts names on cost/token
  counters)
- `OTEL_LOG_TOOL_CONTENT` — "Enable logging of tool content in the `tool.output`
  span event... Requires tracing. Content is truncated at the content limit
  (60 KB by default)"

Source: https://code.claude.com/docs/en/monitoring-usage (common configuration
variables table). The essay's launch block sets all four; names and effects match.
Local status: defaults-off behavior is consistent with tonight's captures (raw
bodies were needed to see content at all), but the flags themselves were not
individually toggled tonight.

## 3. `OTEL_LOG_RAW_API_BODIES=file:<dir>` — untruncated bodies + `body_ref`

**PROVEN, with one caveat.** Docs: the variable emits full request/response JSON
as `api_request_body` / `api_response_body` log events; "`1` for inline bodies
truncated at the content limit (60 KB by default), or `file:<dir>` for untruncated
bodies on disk with a `body_ref` pointer in the event." In file mode Claude Code
also appends one line per successful response to `<dir>/index.jsonl` with fields
`timestamp`, `session_id`, `query_source`, `model`, `request_id`, `message_id`,
`message_uuid`, `request_file`, `response_file` (index requires v2.1.274+).

Local artifacts match exactly:

- `~/agent-logs/claude/raw/index.jsonl` and `~/agent-logs/claude/raw-default/index.jsonl`
  — single lines carrying precisely those nine fields, naming
  `<uuid>.request.json` and `<request-id>.response.json`.
- `~/agent-logs/claude/raw-default/` request body is 82,441 bytes — larger than
  the 60 KB inline cap — confirming file mode is not cut at the content limit.
- File naming and layout match the docs' description.

**Caveat (the essay's "untruncated" needs an asterisk): untruncated ≠ unredacted.**
In both local response files (`req_011CfZ4nsiproz4uToN4QBis.response.json`,
`req_011CfZ527kYLMpJVh9FbrJH6.response.json`) the thinking block's text is the
literal string `<REDACTED>` (signature retained). So file-mode bodies are
size-complete but thinking content is still redacted. Second caveat: the
`body_ref` pointer itself was **not captured locally** — tonight's run used
`OTEL_LOGS_EXPORTER=console` and the console output was not retained; we hold the
files and the index, not the log events. `body_ref` is PROVEN by docs,
UNVERIFIABLE in the local artifacts.

Also terminological honesty (from the earlier docs verification): the bodies are
"JSON-serialized Messages API request parameters" — serialized API JSON, not a
byte-for-byte HTTP wire capture.

## 4. W3C `TRACEPARENT` propagation into Bash/PowerShell subprocesses

**PROVEN (docs); not exercised locally.** Verbatim: "When tracing is active, Bash
and PowerShell subprocesses automatically inherit a `TRACEPARENT` environment
variable containing the W3C trace context of the active tool execution span. This
lets any subprocess that reads `TRACEPARENT` parent its own spans under the same
trace." The same section adds: model requests carry a `traceparent` header set to
the `claude_code.llm_request` span's context (direct Anthropic API connections;
outbound HTTP MCP requests likewise) — with qualifications: the header/subprocess
variable are suppressed when a custom `ANTHROPIC_BASE_URL` proxy is in play unless
`CLAUDE_CODE_PROPAGATE_TRACEPARENT=1`, and inbound `TRACEPARENT` is honored only
in Agent SDK / `-p` sessions (interactive sessions ignore it).

Version scope: several propagation details carry v2.1.212–v2.1.268 floors, all
below the installed v2.1.285.

Local status: **UNVERIFIABLE** — beta tracing was never enabled tonight, so no
subprocess ever received a `TRACEPARENT` here. The essay's "agent trace + app
trace, one trace ID" scenario is real but requires the beta flag on.

## 5. Copilot: `OTEL_EXPORTER_OTLP_ENDPOINT` auto-enables OTel

**PROVEN.** The installed binary's own help (`copilot help monitoring`, saved at
`hidden_files/research/copilot-help-monitoring.txt`): "OTel activates when any of
these conditions are met: `COPILOT_OTEL_ENABLED=true` / `OTEL_EXPORTER_OTLP_ENDPOINT`
is set / `COPILOT_OTEL_FILE_EXPORTER_PATH` is set", and the variable table says of
the endpoint: "Setting this auto-enables OTel." GitHub's docs state the same.
Local nuance: tonight's capture exercised the file-path trigger, not the endpoint
trigger — endpoint-only activation is proven by docs + binary help, not by a
local run.

## 6. Copilot exporter: file **or** otlp-http, mutually exclusive per process

**PROVEN (as documented).** Help text: "`COPILOT_OTEL_EXPORTER_TYPE` — Copilot
exporter backend: `otlp-http` (default) or `file`. Auto-selects `file` when
`COPILOT_OTEL_FILE_EXPORTER_PATH` is set." It is a single selector — one backend
per process — so the essay's "don't make the Copilot process write JSONL and send
OTLP; fan out in the Collector" is architecturally accurate. Two footnotes from
the help text: the path only auto-selects `file` when the type variable is unset,
and with `otlp-http` against an `http://` endpoint (including the default
localhost:4318) "export is disabled rather than sent in cleartext" — silently,
warning only in the process log. Local status: only the `file` backend has been
run here.

## 7. Copilot content capture: `gen_ai.tool.call.arguments` / `gen_ai.tool.call.result`

**Fields PROVEN as documented; presence and shape UNVERIFIABLE in local capture.**
GitHub's content-capture table lists all six side by side:
`gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.system_instructions`,
`gen_ai.tool.definitions`, `gen_ai.tool.call.arguments` ("Tool input arguments"),
`gen_ai.tool.call.result` ("Tool output"). So the essay's field names are real.

But check the actual artifact: tonight's `~/agent-logs/copilot/otel.jsonl`
(33 records = two appended probe runs; the eval's "16 records" counts the first
run's export) contains exactly two span types — `invoke_agent` and
`chat claude-haiku-4-5-20251001` — and the only content keys present are
`gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.system_instructions`,
`gen_ai.tool.definitions`. There is **no `execute_tool` span and no
`gen_ai.tool.call.*` key anywhere in the file**, because both probes were
one-word replies with zero tool calls (`gen_ai.invoke_agent.tool_calls` recorded
0). Per the OTel GenAI conventions these two fields belong on tool-execution
spans, not on the `chat` span — so until someone captures a tool-using Copilot
run under OTel, the claim "turn content capture on and you get tool arguments and
results" rests on GitHub's table alone. E2/E4 provide no evidence either way:
both ran before OTel was enabled (no span/OTel content in
`evals/results/2026-09-30-E2.md` or `...-E4.md`).

## 8. Claude partial `gen_ai.*` vs Copilot's GenAI-convention posture

**PROVEN.** Claude's docs annotate exactly five attributes as borrowed GenAI
conventions — `gen_ai.system` ("Always `anthropic`"), `gen_ai.request.model`,
`gen_ai.response.id`, `gen_ai.response.finish_reasons` on `claude_code.llm_request`,
and `gen_ai.tool.call.id` on the tool spans — each explicitly labeled
"OpenTelemetry GenAI semantic convention," while the span names and the bulk of
attributes (`model`, `input_tokens`, `duration_ms`, `ttft_ms`...) are
Claude-specific. "Hierarchy primarily `claude_code.*`, several GenAI-standard
fields too" is accurate.

Copilot's help opens with: "All signal names and attributes follow the OTel
GenAI Semantic Conventions, so the data works with any OTel-compatible backend."
Tonight's capture backs this: every attribute on the `chat`/`invoke_agent` spans
is `gen_ai.*` or standard (`server.address`, `enduser.pseudo.id`) — with a vendor
tail (`github.copilot.cost`, `github.copilot.context.skills`,
`github.copilot.mcp.server.connection.count` metric). So "Copilot is more
standardized at the schema layer" holds; "purely standard" would not. The essay's
recommended strategy (canonical model on `gen_ai.*`, vendor adapters for the
rest) matches this observed reality.

## 9. Copilot hierarchy `invoke_agent` → `chat` / `execute_tool`

**Half PROVEN locally, half PROVEN by docs only.** The installed binary's help
draws the tree verbatim:

```
invoke_agent
  plan
    chat <model>
    execute_tool <tool>
  chat <model>
  execute_tool <tool>
```

Tonight's capture confirms the top of it: `invoke_agent` root (span kind
internal) with child `chat claude-haiku-4-5-20251001` (kind client,
`parentSpanId` = the `invoke_agent` span's ID, same `traceId`), plus
`github.copilot.mcp.server.lifecycle`, `github.copilot.user.message`, and
`github.copilot.session.usage_info` span events on the root. But **no
`execute_tool` span has ever been captured locally** — both OTel probes made
zero tool calls, and E2/E4 predate OTel. The sub-tree (`execute_tool`, `plan`)
is documented-but-unobserved on this machine, and with it the exact placement of
claim 7's two fields.

---

## Extra check: skill and hook spans (the essay's canonical event list assumes both)

- **Copilot: neither exists in the telemetry surface.** The string `skill`/`hook`
  does not appear in `copilot help monitoring` at all. Skills surface only as an
  attribute on `invoke_agent` — `github.copilot.context.skills`, observed tonight
  as `["customize-cloud-agent","github-pr-media"]`. There is no hook span or
  event (and per E4, repository hooks don't even execute on v1.0.89). A
  normalizer emitting canonical `skill`/`hook` events from Copilot spans would
  be inventing structure the exporter doesn't have.
- **Claude: hook = real but deeply gated; skill = not a span.** Hook executions
  are children of `claude_code.interaction`, and a dedicated `claude_code.hook`
  span exists (`hook_event`, `hook_name`, `num_hooks`, ...) — but **only under
  detailed beta tracing** (`ENABLE_BETA_TRACING_DETAILED=1` +
  `BETA_TRACING_ENDPOINT`, which also reroutes logs/traces, and needs an org
  allowlist for interactive CLI sessions). The plain enhanced-telemetry beta
  does not produce it. Skill invocation has no span of its own: a skill call is a
  `claude_code.tool` span for the Skill tool, carrying a `skill_name` attribute
  gated by `OTEL_LOG_TOOL_DETAILS`.

So of the essay's canonical events, `hook` maps to one tool (Claude, behind a
second beta gate) and `skill` maps to neither tool's span model. The normalizer
would synthesize both — feasible, but they are derived events, not observed ones.

## Where the essay's pipeline overlaps agent-setup vs what's genuinely new

The essay's loop — OBSERVE (spans) → UNDERSTAND (attributes/content/raw body) →
REACT (hooks) → LEARN (normalizer + evaluator) → PERSIST (note/lesson) →
PROMOTE (skill) — terminates in exactly the layer agent-setup already runs, the
file-based one Karpathy's llm-wiki gist describes:

**Already implemented via files (proven tonight):**

- PERSIST: `wiki/notes/` + `wiki/index.md` + `wiki/log.md` — the llm-wiki
  pattern (immutable raw sources → maintained interlinked Markdown → schema in
  AGENTS.md). E2 proved cross-tool continuity from these files (5/5 probes);
  E5 proved active-only retrieval cuts orientation tokens 38% at zero quality
  drop. The wiki compounds knowledge today with no Collector.
- PROMOTE: durable lessons already become `canonical/` skills/agents installed
  into both tools (`session-harden` is the worked example; E1 PROVEN).
- OBSERVE (partial): tonight's raw API bodies (Claude) and OTel JSONL (Copilot)
  were captured by simply setting env vars — the essay's "learning/debug mode"
  already works here ad hoc; the harness-overhead decomposition
  (`evals/results/2026-09-30-otel-instrumentation.md`) was done by parsing those
  files directly, no normalizer.
- REACT (partial): the failure-capture hook + sidecar works on Claude
  (`PostToolUseFailure`, 5/5 — E4) and is REFUTED on Copilot v1.0.89.

**Genuinely new machinery the essay adds:**

- An **always-on, structured event stream** (Collector on localhost:4318, trace
  DB) instead of per-investigation captures: queryable durations, permission-wait
  time, retry/TTFT, parent-child causality across turns — none of which the file
  captures retain once the session ends.
- **Cross-process correlation**: `TRACEPARENT` into Bash/PowerShell subprocesses
  (claim 4) so application errors join the agent's trace — impossible with
  session transcripts.
- A **normalizer + evaluator at machine speed**: canonical events
  (`model.request`, `tool.request/result`, `permission`, `compaction`) computed
  continuously, versus tonight's manual per-question file parsing. This is the
  only part that changes the *learning loop's* economics; the wiki already
  handles the knowledge half.
- Coverage where files are blind: tool-level signal from Copilot (hooks don't
  run there; OTel `execute_tool` spans are the only documented route — and per
  claims 7/9, still uncaptured locally).

**Debate-sharpening gap:** the essay's canonical event list assumes `skill` and
`hook` events; per the extra check, neither tool emits those as spans today
(Claude: hook only under detailed beta tracing; skill = tool span + gated
attribute; Copilot: neither). And its two most load-bearing Copilot claims
(tool arguments/results on spans) are doc-proven but have never been observed on
this machine. The architecture is sound; its evidence base on the Copilot side
is currently GitHub's documentation, not captures.
