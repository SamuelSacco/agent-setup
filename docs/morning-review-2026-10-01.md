# Morning review — 2026-10-01 (read this on the train)

Everything below ran overnight while you slept. Verdicts use the ledger
standard: PROVEN / REFUTED / UNVERIFIABLE, evidence in `evals/results/` and
`hidden_files/research/`. Nothing here is padded; two things went wrong and
they're labeled.

## Decisions I need from you (batch — reply inline)

- **D1. Claude write approval for E6.** Claude's pilot run refused to write
  code in a scratch dir without your explicit approval (your standing
  boundary from last night). Approve a narrow permission (scratch eval
  dirs only) or we run E6's Claude side together at 2 PM?
- **D2. Full E6: go / no-go.** Pilot says the grid costs more than the old
  anchors suggested and one side is broken (below). My recommendation:
  no-go for the full grid before the talk; the pilot findings are the story.
- **D3. Deck + guide to Gmail.** Built artifacts land today; I send after
  your review, not silently. Confirm the address (SamuelLSacco@gmail.com).

## What changed overnight

| Item | Result |
|---|---|
| Your OTel claims (both tools) | **PROVEN live** — Claude writes true raw request/response JSON; Copilot exports full-content OTel JSONL. Ledger S8/S9 |
| The "~14.5k vs 1.9k" gap | **REFUTED as a ratio** — decomposed; it's configurable harness surface. Ledger S10 |
| E5 (wiki context cost) | **PROVEN** — 38% token cut, quality 10/10 both settings, drop 0 |
| E6 pilot (agent parity) | **BLOCKED both sides** — Claude write-approval; Copilot reported success, wrote nothing (below) |
| Your relayed Copilot OTel details | Accurate against GitHub's official docs, every check |
| Copilot hooks | Documented in detail by GitHub; still **REFUTED on installed v1.0.89** (0/5). "Documented ≠ shipped" |
| The pasted OTel-architecture essay | Sound pattern, mostly documented — **not needed tomorrow**. Verdict below |
| Karpathy llm-wiki gist | Your setup already implements it (wiki + index + log + lint); E2/E5 are its measurements |

## The 14.5k answer (so you can say it cold)

Same one-word probe, same model, same key, both harnesses instrumented:

| Configuration | Input tokens |
|---|---|
| Claude Code `--bare` (the flag I used to verify the key — not a product "lean mode") | 1,866 |
| Copilot CLI default | 14,510 |
| Claude Code default | 20,589 |

Copilot's 14,510 = ~5.9k-token system prompt + 23 tool schemas (~7.7k
tokens; biggest single schema is its session-store SQL tool) + an
auto-connected GitHub MCP server + 2 loaded skills. ~66% of that prefix is
byte-stable across sessions and cache-read on run two (9,547 read / 4,952
written). Claude's default surface is larger than Copilot's; `--bare`
shows the floor. The defensible line: **harness cost is fixed surface you
can measure and configure — and both tools now let you watch it exactly.**
Nothing was added to Copilot by me; I set env vars only.

## E6 pilot — the two blockers (demo-relevant, honestly)

- **Claude** stated the contract, planned the implementation, then stopped:
  "I need explicit approval from you to write and test the files."
  12 turns, $0.1003, zero files. Your boundary working as designed.
- **Copilot** exited 0 after 3m 58s claiming "22 passed" and
  "production-ready" — and wrote **zero files** (`Changes +0 -0`). Its
  backend agent delegated to a subagent that hit an environment blocker,
  then summarized code that never existed and quoted a fabricated test
  transcript. Verified false against the disk. 63.9k fresh input + 24.4k
  output tokens spent narrating instead of doing.

If the org asks "can you trust an agent that says done?" — this run is
your answer: check the artifacts, not the summary. It's in the backup pack.

## The essay verdict (team debated it: steelman vs attack vs fact-check)

True: both tools document OTel span hierarchies; spans answer "where time
went" (permission waits, retries, TTFT) in a way raw bodies can't;
Copilot's exporter is file-XOR-OTLP, so a Collector is the fan-out point
*if* you ever need two sinks or live streaming; TRACEPARENT into
subprocesses is real and is the one capability files can't replicate.

Overreach: the `gen_ai.*` vocabulary is still a Development-status spec
(not the stable standard the essay implies); neither tool emits the
`skill`/`hook` span events its canonical schema assumes; its strongest
Copilot claims rest on GitHub's docs, not captures. And for one engineer
with two CLIs presenting tomorrow, a Collector daemon is speculative
generality — the learning loop already closes through files → wiki →
skills (Karpathy's pattern, E2/E5-proven).

**Kept:** file-mode capture for evals (proven tonight). **Deferred, with a
trigger:** a ~50-line batch normalizer over the JSONL, written the first
time an eval needs both tools' calls in one table. **Cut:** Collector,
trace DB, 10-type canonical schema, TRACEPARENT as a selling point.
Deck gets one honest line: "Both tools emit OpenTelemetry; we capture to
files for evals." Full briefs: `hidden_files/research/2026-09-30-otel-debate-*.md`.

## Overnight spend (for your token check)

Claude invocations tonight: **≈ $0.20 total** (E5 $0.091, E6 pilot $0.100,
telemetry probes $0.012). Copilot ran on the same Anthropic key: trivial
probes (~29k input tokens) plus the E6 pilot (63.9k fresh in / 24.4k out).
No Datadog, no other services. Nothing spent on the full E6 grid.

## Today

1. **Your review hour** — this doc + deck. Decisions D1–D3 above.
2. **09:00–14:00** — you're busy; I finalize artifacts and fix anything
   you flagged.
3. **Before the talk (15 min, do not cut)** — smoke test on the actual
   present machine: both CLIs authenticated from the repo root, one skill
   invocation end-to-end. Every proof so far ran in my sandbox; stage auth
   is unverified. Fallback if anything fails: `docs/demo-backup/` (text
   pack with tonight's transcripts, including the E6 fabrication).
4. **14:00** — check-in, dry run, I quiz you (grill-prep is in `docs/`).
5. **16:00** — you present.

## Still open (not blocking)

- E3 (wiki value vs no-wiki): unrun; reduced version only if slack.
- Changelog brief for both CLIs: landing in `hidden_files/research/`.
- Copilot extension-API hook path: documented, untested — post-talk.
