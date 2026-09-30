# OTel debate — the case for spans as canonical signal (ADVOCATE brief)

Date: 2026-09-30. Scope: Claude Code + Copilot CLI only (the essay's Codex
mentions are out of scope per instructions). Verdicts per repo convention:
**PROVEN** / **REFUTED** / **UNVERIFIABLE**. Evidence: tonight's live captures
(`evals/results/2026-09-30-otel-instrumentation.md`, `~/agent-logs/`),
official Anthropic monitoring docs (code.claude.com/docs/en/monitoring-usage,
read 2026-09-30), official GitHub docs + the locally shipped
`copilot help monitoring` text (`hidden_files/research/copilot-help-monitoring.txt`),
and the OTel GenAI semantic-conventions repo.

## What the essay claims, restated

1. OTel spans — not raw API bodies — should be the canonical cross-agent
   signal; raw bodies are a high-fidelity side channel attached by reference.
2. Both CLIs should export OTLP to one Collector on localhost:4318, which
   fans out to a raw archive, a trace DB, and a normalizer.
3. The normalizer emits canonical events (session/turn, model.request,
   tool.request, tool.result, hook, skill, permission, compaction).
4. Hooks react; spans observe; the normalizer learns; lessons persist to
   notes and promote to skills.
5. Claude propagates W3C TRACEPARENT into subprocesses, so application spans
   join the agent's trace.

## Baseline: what tonight already proved (the steelman must beat this)

File captures work, end of story: Claude wrote untruncated
request/response JSON plus `index.jsonl` (`OTEL_LOG_RAW_API_BODIES=file:<dir>`);
Copilot wrote a 16-record full-content OTel JSONL from one env var
(`COPILOT_OTEL_FILE_EXPORTER_PATH`, with
`OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`). From those files
alone we decomposed Copilot's 14,510-token input to the tool definition
(session_store_sql 6,701 chars, task 3,303, bash 2,840), and refuted the
naive "Copilot wastes tokens" ratio (Claude `--bare` 1,866; Copilot default
14,510; Claude default 20,589). The essay's architecture has to justify
itself against *that*, not against ignorance.

## Verdicts on the essay's load-bearing claims

| Claim | Verdict | Basis |
|---|---|---|
| Claude exposes `claude_code.interaction` → `llm_request` / `tool` (→ `blocked_on_user`, `execution`) spans; tracing is beta | **PROVEN** | Anthropic docs: "Each user prompt starts a `claude_code.interaction` root span… Tool spans have two child spans of their own: one for the time spent waiting on a permission decision and one for the execution itself." Enabled via `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` + `OTEL_TRACES_EXPORTER`; section header literally "Traces (beta)" |
| Copilot exposes `invoke_agent` → `chat` / `execute_tool` per OTel GenAI conventions | **PROVEN** | `copilot help monitoring` span tree; GitHub docs: "All signal names and attributes follow the OTel GenAI Semantic Conventions" |
| Copilot exporter is file XOR otlp-http, never both | **PROVEN** | Help text: `COPILOT_OTEL_EXPORTER_TYPE` is one value, `otlp-http` (default) or `file`; file exporter "never resolves an OTLP endpoint" |
| Claude raw bodies: untruncated files on disk + `body_ref` in the event | **PROVEN** | Docs for `OTEL_LOG_RAW_API_BODIES`; tonight's `~/agent-logs/claude/raw/index.jsonl` carries `request_file`/`response_file` per line (needs v2.1.274+) |
| Claude propagates TRACEPARENT into Bash/PowerShell subprocesses | **PROVEN, with conditions** | Docs: "When tracing is active, Bash and PowerShell subprocesses automatically inherit a `TRACEPARENT` environment variable…" Conditions: tracing must be on; model-request header propagation is suppressed for third-party `ANTHROPIC_BASE_URL` unless `CLAUDE_CODE_PROPAGATE_TRACEPARENT=1`; and `OTEL_*` exporter config is explicitly *not* passed to subprocesses — only the trace context travels |
| `gen_ai.*` is a stable canonical vocabulary you can build on directly | **REFUTED as stated** | The GenAI conventions live in `open-telemetry/semantic-conventions-genai` with document status **Development**; attributes carry Development badges and names are still churning (`gen_ai.system` → `gen_ai.provider.name`; Claude emits the old `gen_ai.system`, Copilot the new `gen_ai.provider.name` — both observed in tonight's sources). Usable, shipping, but not frozen |
| A Collector is necessary for a single-user two-CLI setup | **UNVERIFIABLE** (judgment, argued below) | Mechanism is real; necessity depends on concurrency and live-monitoring needs |

## What spans + normalization genuinely buy beyond tonight's files

**1. Where the time went — the question raw bodies cannot answer.**
A raw request body is a snapshot of one API call. It says nothing about
permission waits, retries, or tool runtime. Claude's span tree splits a tool
call into `blocked_on_user` (with `duration_ms` and the accept/reject
`decision`) and `execution` (`duration_ms`); `llm_request` carries
`ttft_ms`, `attempt`, `error_class`, `success`. Copilot's metrics carry
`gen_ai.client.operation.time_to_first_chunk` and
`gen_ai.execute_tool.duration`. "The agent hung for three minutes" is a
span query; from raw bodies it is unanswerable at any fidelity. **PROVEN**
(both vendors document the fields; Copilot's were in tonight's JSONL).

**2. Cross-tool comparison becomes one query instead of two parsers.**
Tonight's decomposition used two unrelated methods: hand-measuring
serialized Anthropic JSON fields on the Claude side, and parsing vendor
OTel attribute JSON on the Copilot side. That worked once. The eval suite
(E1–E6) and any recurring cost/latency tracking repeat the same questions —
tokens per call, cache read/write split, tool error rate, TTFT — against
both tools. Canonical `model.request` events make each of those one query
instead of two code paths. Note the asymmetry that forces a *thin*
normalizer rather than direct use of `gen_ai.*`: Claude's `llm_request`
already sets GenAI attributes (`gen_ai.request.model`,
`gen_ai.response.id`, `gen_ai.response.finish_reasons`, `gen_ai.tool.call.id`
per docs) but keeps Claude span names, while Copilot is GenAI-native
throughout. The mapping is renames and hoisting, not semantic extraction —
which is precisely why it's cheap. And because the GenAI spec is still
Development-status, a small canonical layer of our own insulates eval
queries from upstream renames. The essay's strongest sentence is its own
defense: build canonical events, adapt at the edge. **Mechanism PROVEN;
payoff is proportional to how often the question repeats.**

**3. Structure that content flattens: subagents, hooks, permissions, retries.**
Claude nests subagent spans under the parent `claude_code.tool` span with
`agent_id`/`parent_agent_id`; Copilot "automatically links subagent
invocations into the same trace via context propagation" (help text). E6
(agent parity across tools) needs exactly this graph; raw bodies flatten it
into message soup you'd reconstruct by hand. Likewise, hook executions are
spans in Claude's tree, permission decisions are span attributes, and
retries are `gen_ai.request.attempt` span events — none of these exist in
any API body. This matters most where tonight hurt: E4's Copilot hook
result (0/5, REFUTED on v1.0.89) had to be established by a dedicated
experiment. With canonical hook events, "hook fired 0 times in N sessions"
is a query that returns a negative — and negatives are what a claims ledger
runs on. **PROVEN (documented surfaces); the E4 application is direct
experience, not speculation.**

**4. The one capability no file capture provides at any fidelity:
TRACEPARENT causality across the agent/app boundary.** The essay's frontend
example is concrete: Claude runs `npm run dev` via Bash; the subprocess
inherits `TRACEPARENT`; an instrumented dev server parents its spans —
including the TypeError — under the same trace as the agent's Edit and tool
spans. Tonight's files can reconstruct what the model saw and said; they
cannot join "agent edited file" → "server crashed" into one causal chain
with timings. This is the demo-grade capability for an org talk, and it is
uniquely span-shaped. Honest conditions: tracing must be enabled, the app
must read `TRACEPARENT` and export its own spans, and `ANTHROPIC_BASE_URL`
proxies gate the header path. **PROVEN as a documented mechanism;
UNVERIFIABLE for any specific app until tried.**

**5. Fan-out is the Collector's real job, and Copilot's exporter design
forces it.** Copilot gives you file XOR otlp-http — one sink, chosen per
process. The moment you want Copilot spans both archived as JSONL *and*
live in a trace backend, the fan-out must happen downstream of the single
exporter: that is the Collector. Same for policy asymmetry: Claude's
content gates are four separate flags (`OTEL_LOG_USER_PROMPTS`,
`OTEL_LOG_ASSISTANT_RESPONSES`, `OTEL_LOG_TOOL_DETAILS`,
`OTEL_LOG_TOOL_CONTENT`) plus a 60 KB truncation limit; Copilot's is one
flag. A Collector-side pipeline can enforce one retention/redaction policy
over both. The essay's two modes (metadata-only normal operation,
everything-on learning mode) map to documented defaults on both vendors —
content capture is opt-in and off by default on each. **PROVEN mechanism.**

## When the live Collector beats post-hoc file parsing — and when it doesn't

Collector pays when: both CLIs run concurrently and you need one
interleaved timeline keyed by trace ID; you want live signals (error-class
spikes, latency regressions after a CLI upgrade — both tools rev weekly,
and tonight's docs alone carry version gates at v2.1.214/268/274/281/283);
multiple developers feed one backend (cost per repo per day is already a
metric on both sides — `claude_code.session.count` and the
`gen_ai.client.inference.usage.*` counters); or you need the dual-sink
fan-out above.

Files win when: one user, post-hoc evals, offline or CI (Copilot's own
help lists file output as the "offline / CI" mode), zero new long-lived
processes. Everything proven tonight was file-based. The Collector is an
operational commitment; files are an artifact. For the org talk, files are
the proof and the Collector is the scaling story — that ordering is honest.

## The Karpathy question: what does the normalizer feed the wiki that tonight's captures don't?

agent-setup already implements the llm-wiki pattern — immutable raw sources,
LLM-maintained interlinked notes (`wiki/notes/`), `index.md` as catalog,
`log.md` append-only, `wiki-lint`, schema in AGENTS.md — with E2 (cross-tool
continuity from the wiki) and E5 (active-only retrieval, 38% token cut,
zero quality drop) PROVEN. The essay's observe→learn→persist→promote loop
terminates in exactly this layer. So the normalizer does not add a memory
system; it changes what the existing memory eats. Today the wiki's
behavioral inputs are: agent-written session records (self-reported,
lossy, written by the system being described), the hook sidecar (Claude
PROVEN, Copilot REFUTED as of E4), raw bodies (exact, but per-request and
unaggregated), and OTel JSONL (complete, but vendor-shaped, one file per
run). Canonical events add three things none of those provide:

- **Computed facts instead of narratives.** Median TTFT per tool,
  permission-wait share of turn time, retry/error-class rates, cache
  stability (tonight's "66% of prefix byte-stable" came from two spans; as
  a canonical metric it's a standing row). The wiki pattern's ingest step
  is distillation — the normalizer is a mechanical distiller feeding the
  LLM distiller, and its outputs arrive pre-aggregated enough to cite.
- **Negatives at scale.** "Copilot hooks fired 0/40 sessions" as a query
  result is a ledger-grade claim. Tonight that took a bespoke experiment;
  with canonical hook events it's lint output, and wiki notes gain
  refutation evidence without new experiments.
- **A freshness signal for tool-behavior claims.** `wiki-lint` currently
  checks notes' `verified` dates. Canonical events keyed by app version
  let it ask the harder question: "the 14.5k surface claim was verified on
  v1.0.89; we've since captured v1.0.9x spans — does it still hold?" That
  closes Karpathy's lint loop on the claims that rot fastest.

Honest limit: the normalizer makes the wiki's inputs denser and less
self-reported; it does not make the wiki smarter. The wiki remains the
memory. Spans become its best raw source — `wiki/raw/` tier, machine-made.

## The smallest version that captures ~90% of the value

1. **One Collector, later.** Start with zero new daemons: keep tonight's
   file captures, and add ONE batch normalizer script that reads Claude's
   raw-body dir (join key: `index.jsonl` `request_id` ↔ span `request_id`)
   and Copilot's OTel JSONL, and emits canonical-events JSONL with
   `raw_ref` pointers. Eight event types is the whole schema.
2. **One consumer.** A lint pass that diffs canonical aggregates against
   `docs/claims-ledger.md` verdicts and drafts wiki-note updates. No trace
   DB until a second developer needs one; Jaeger/Tempo earn their place at
   org rollout, not before.
3. **Add the Collector when the first dual-sink or live need appears**
   (Copilot file-vs-backend is the forcing case). Both CLIs already speak
   OTLP/HTTP to `localhost:4318`; the env blocks are proven patterns from
   tonight.

## Risks the advocate must concede

- Claude tracing is **beta**; its span attributes are version-gated all
  through the docs. The normalizer must treat every attribute as optional,
  or the first CLI upgrade breaks the pipeline. (This cuts for the
  canonical layer, not against it: vendor churn is the argument.)
- Capture-mode asymmetry corrupts naive comparisons: a missing tool result
  in canonical events can mean "not captured" (gates off) rather than
  "didn't happen." Canonical events must record the capture mode that
  produced them, or cross-tool diffs lie.
- Claude's detailed beta tracing can reroute logs/traces to
  `BETA_TRACING_ENDPOINT`, bypassing the configured exporters — a config
  gotcha the Collector plan must pin down.

## Bottom line

The essay is right about the load-bearing thing: spans are the only signal
that carries causality, timing structure, and lifecycle events in a shape
two different vendors already emit. Tonight proved files are sufficient to
*answer a question once*; the normalizer is what makes the answers
*repeatable, comparable, and self-updating* — and it feeds a wiki that
already knows what to do with them.
