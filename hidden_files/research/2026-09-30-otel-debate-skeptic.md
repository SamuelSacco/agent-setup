# OTel debate — skeptic brief

Written 2026-09-30 ~01:50 EDT. Read-only; no CLIs run, nothing committed.
Target: the pasted essay proposing OTel spans as canonical cross-agent
signal, a Collector on localhost:4318, a normalizer emitting canonical
events, and a trace DB — for one engineer, two CLIs, presenting Oct 1.

## Verdict

The essay's facts are mostly right and its conclusion is mostly wrong for
us. It designs the observability stack of a *product* (N agent runtimes, a
fleet, eval pipelines) and offers it to a *practice* (one engineer, two
CLIs, a wiki, a presentation tomorrow). Everything in it that we would
actually use, we already proved tonight with files. Everything else is a
daemon in search of a consumer.

## Fact-check: the essay vs our evidence

| Essay claim | Verdict |
|---|---|
| Copilot spans: `invoke_agent` root, `chat` / `execute_tool` children | **PROVEN** — docs; `invoke_agent` + `chat` observed live in `~/agent-logs/copilot/otel.jsonl`; `execute_tool` documented but not yet exercised (our probe called no tools) |
| `OTEL_EXPORTER_OTLP_ENDPOINT` / file path auto-enable Copilot OTel; file OR otlp-http exporter | **PROVEN** — docs + live (S9) |
| Content capture fields incl. `gen_ai.provider.name` | **PROVEN** — docs; system instructions, tool definitions, input messages observed live |
| Claude raw bodies: `file:<dir>` untruncated, `body_ref`, `index.jsonl` | **PROVEN** — docs + live files on disk (S8) |
| Claude span tree `claude_code.interaction / .llm_request / .tool / .blocked_on_user / .execution` | **UNVERIFIABLE** — absent from the official monitoring-docs sweep; never enabled in a live run. Our Claude evidence is log events + body files, not one span |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` as the switch for that tree; "tracing marked beta" | **UNVERIFIABLE** — not in our docs verification. The Claude half of the architecture diagram rests on its least-verified plank |
| Claude → OTLP via HTTP/protobuf, HTTP/JSON, gRPC | **UNVERIFIABLE** — our docs evidence covers exporter *types* (`console`, `otlp`, `none`), not protocols |
| W3C TRACEPARENT propagated into Bash/PowerShell subprocesses | **UNVERIFIABLE** — not in our docs sweep; and worthless here regardless (see §4) |
| "Copilot is more standardized; Claude also exposes GenAI fields" | **PARTIAL** — Copilot's `gen_ai.*` attributes are PROVEN live. The only complete Claude capture we hold is proprietary Messages-API JSON with zero `gen_ai.*` vocabulary. The essay's premise — "use GenAI attributes directly, vendor-adapt the gaps" — is asymmetric in a way it waves past: for Claude, the gaps are the whole signal |
| Canonical events incl. `permission`, `compaction` | **REFUTED as span-derived, today** — no observed span emits either. Both tools surface compaction/permission only as *hook* events (docs), and Copilot repo hooks are REFUTED on our build (E4: 0/5, binary-forensics: zero hook events in 8 session logs). The schema designs events whose sources don't fire |

The essay says "Claude Code now officially exposes this hierarchy" —
"officially" doing the lifting, uncited. Our own official-docs pass found
logs, metrics, and raw-body events. The span tree may exist upstream; on
our evidence it is a rumor with good posture.

## The scale error

Count the moving parts the essay asks for: OTLP/protobuf ingestion, a
Collector daemon (config, pipelines, upgrades), a raw archive, a trace DB,
a normalizer, a 10-type canonical event schema, metrics and logs pipelines,
two-mode env management. Now count the telemetry questions actually asked
in this project so far: one. "Why did Copilot spend 14.5k tokens on OK?"
It was answered tonight with one env var, one JSONL file, and a short
Python decomposition — no Collector, no normalizer, no protobuf (S10,
`evals/results/2026-09-30-otel-instrumentation.md`). Our entire evening of
Copilot telemetry is 33 JSONL lines; Claude's is three JSON files and a
one-line index. At this volume, the query engine is `grep` and the trace
DB answers a question — "show me the waterfall" — that nobody has asked.

The essay's modality is the tell: agents' code "*can* join the same
trace," raw bodies "*would* just be attached," the abstraction is "exactly
the abstraction you want." Want for what? It never names a consumer. Our
evals (E1–E6) read transcripts, session records, CLI footers, and the
sidecar JSONL. No eval reads spans; no alert exists; no dashboard exists;
the "learner" is an LLM session — which reads files natively. The
Collector/normalizer would be two infrastructure layers inserted between
evidence we already hold and readers who already read it.

And the generality is smuggled scope: the design's payoff case is
"as soon as you introduce Copilot, Codex, Gemini CLI, OpenCode."
Samuel scoped this to two tools and explicitly cut Codex. Optimizing for
a fleet we don't operate is the definition of speculative generality.

## The learning loop already closes (Karpathy point)

The essay's pipeline terminates at canonical events → evals → lessons →
skills → shared skills dir. That terminal layer exists, is ours, and is
proven: `wiki/notes/` + `wiki/index.md` + `wiki/log.md` + wiki-lint is
Karpathy's llm-wiki pattern; E2 PROVEN (a cold tool continued the other
tool's session from these files, 5/5, with a clean no-wiki control that
invented nothing); E5 PROVEN (archiving cut context 38% at zero quality
drop). Its inputs today are session records, eval results, and sidecar
events — all files, all readable by either agent directly. For a span to
teach the wiki anything it must be captured, normalized, read by an LLM,
and distilled into a note. Steps one and two are the entire essay; step
three demonstrably works on the raw files (the 14.5k decomposition *was*
an LLM reading the JSONL and request JSON). The proposed stack lengthens
a loop whose measured bottleneck is zero layers. Worse: Karpathy's point
is that maintenance cost near zero is the whole game — a Collector is
maintenance with a config file.

## Where I concede (steelman, honestly)

- **Live signal.** Spans stream; files are post-hoc. If Samuel ever wants
  a mid-run "the agent is blocked on a permission prompt" view, OTLP gives
  it and files don't. Genuine — and useless tomorrow: nobody watches a
  dashboard while operating their own deck.
- **In-flight correlation.** For a long, failure-heavy session, a span
  tree (which tool call hung under which model request, with durations)
  beats grepping interleaved logs. Real. It argues for the Copilot *file
  exporter* during debugging — which we have — not for a Collector.
- **The vocabulary.** `gen_ai.*` attribute names are the right words if a
  normalizer is ever written; Copilot already emits them, and adopting
  the names in our sidecar costs nothing. Concede the words, reject the
  plumbing.
- **The observe/react split.** Spans observe, hooks react — correct, and
  already our architecture (E4). Noting, skeptically, that on Copilot
  v1.0.89 the react half doesn't fire for repo hooks at all; the essay's
  symmetric two-legged diagram is docs-true and build-false on one leg.

## Cost of being wrong

- **Tonight.** Remaining hours are allocated (path-forward §1: deck
  factual pass, E5 quality axis, E6 gate, grill refresh, artifact builds,
  commit/freeze). The cut order never contemplates telemetry infra,
  because the talk doesn't depend on it. Every Collector hour is taken
  from the dry run.
- **On stage.** Path-forward names environment transfer as the #1 risk
  and budgets a 15-minute smoke test for the *current* setup. A Collector
  adds a daemon that must be running, on the right port, with both CLIs
  pointed at it — and OTLP exporters fail silently into a dead port, so
  the failure mode is an empty demo discovered live. Files already on
  disk cannot fail that way.
- **Epistemically.** Our own rules (AGENTS.md §5, the ledger, path-forward
  §5 "never fake") forbid presenting unbuilt machinery as the system. A
  Collector slide tomorrow is UNVERIFIABLE wearing a PROVEN costume — the
  exact offense this project exists to not commit.
- **Security.** Full-content mode centralizes prompts, source, and tool
  output into one always-on store. GitHub's own docs: "Content capture
  may include sensitive information such as code, file contents, and user
  prompts. Only enable this in trusted environments." Samuel is mid
  data-broker-removal sweep with a standing boundary about unmonitored
  agent access. Scoped per-probe files are a deliberate act; a Collector
  normalizes collecting everything by default.

The asymmetry settles it: skipping the Collector is reversible (JSONL
files replay into any future backend), building it tonight is not (beta
span renames, stage failure, hours gone). Reversible-later beats
irreversible-tonight, every time.

## Minimum useful subset

1. **Keep (status quo, all PROVEN):** file-mode capture for evals and
   debugging — Claude `OTEL_LOG_RAW_API_BODIES=file:<dir>` (bodies +
   `index.jsonl`), Copilot `COPILOT_OTEL_FILE_EXPORTER_PATH` with content
   capture when the question needs content. This is the essay's
   "learning/debug mode" with the daemon amputated.
2. **Defer, with a trigger:** a ~50-line *batch* script over the JSONL +
   request JSON emitting the handful of fields evals actually consume
   (model, tokens, cache, duration, tool, success) into the existing
   sidecar — written the first time an eval needs both tools' calls in
   one table, using `gen_ai.*` names. Not before, not as a service.
3. **Calendar note, post-presentation:** re-check Claude tracing status
   (beta?) and Copilot hook execution on newer builds — E4's open gap.

## Cut entirely

- Collector daemon, localhost:4318, protobuf — ops burden, stage risk,
  zero consumers.
- Trace DB / waterfall backend — answers an unasked question.
- OTLP metrics/logs pipelines — the JSONL already carries the metrics
  records we use.
- The 10-type canonical event schema — designed ahead of demand; two of
  its types have no firing source.
- TRACEPARENT-into-subprocesses as a selling point — needs instrumented
  child apps; we run none; agent-setup has no frontend to trace.
- Codex/Gemini/OpenCode readiness — out of Samuel's stated scope.
- Any of it on a slide tomorrow as built. At most one honest line:
  "Both tools emit OpenTelemetry; we capture to files for evals."
  That line is PROVEN (S8, S9). The rest is a research direction, and
  the deck already knows how to label those.
