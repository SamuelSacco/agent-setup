# The feedback loop

How an adopter runs the loop on this setup — capture, review, judge,
improve — with the exact commands. Every step is labeled with how it
actually runs today: **automatic**, **agent-run**, or **manual**. No step
is a daemon. Nothing here phones home; telemetry stays on local disk
(it can contain prompts and code — redact excerpts before sharing).

## 1. Capture — what a session leaves behind

- **Session records** — `wiki/sessions/<date>-<time>-<tool>-<slug>.md`,
  written during the session per AGENTS.md §2 (template:
  `wiki/sessions/TEMPLATE.md`). **Agent-run.**
- **Failure events** — `canonical/hooks/failure-capture.json` defines a
  `tool_failure` hook; adapters render it per tool and the sidecar
  appends structured events to `wiki/telemetry/events.jsonl`.
  **Automatic where the tool delivers the event** — and delivery is
  asymmetric today (ledger S4): Claude `PostToolUseFailure` PROVEN 5/5;
  Copilot hooks are directory-trust gated and its `postToolUseFailure`
  does not fire for shell exit failures (the exit code sits in the
  `postToolUse` payload). Copilot failure capture is therefore PARTIAL;
  the payload-parsing adapter is identified, not built.
- **Telemetry (OTel, file mode)** — enabling is a **manual** env step;
  once set, export is **automatic**:
  - Claude Code: `CLAUDE_CODE_ENABLE_TELEMETRY=1` +
    `OTEL_LOG_RAW_API_BODIES=file:<dir>` → raw request/response JSON +
    `index.jsonl` (ledger S8). This is the serialized API body, not a
    byte-for-byte wire capture.
  - Copilot CLI: `COPILOT_OTEL_FILE_EXPORTER_PATH=<file>` alone enables
    export; add `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`
    for full message content (ledger S9). The export is a GenAI-semantic
    representation, not the literal provider request body.

## 2. Review — session close

- Invoke the **session-harden** skill by name in either tool
  (`canonical/skills/session-harden.md`; invocable in both, ledger
  S1/S14). It distills the session's `## Learned` into `wiki/notes/`
  (schema: `wiki/data-model.md`), updates `wiki/index.md`, appends
  `wiki/log.md`, and closes the session record. **Agent-run** — invoked
  at close, not scheduled.
- **wiki-lint** (`canonical/skills/wiki-lint.md`) applies the note
  lifecycle on demand: active → stale → archived. **Agent-run.**
- Repeated failures in `wiki/telemetry/events.jsonl` or a session log
  become one of: a wiki note, a canonical fix, or a new eval task.
  That triage is **manual/agent judgment** today.

## 3. Judge — the claims ledger

- `docs/claims-ledger.md` is the scoreboard: every system claim carries
  **PROVEN / REFUTED / UNVERIFIABLE / PARTIAL** plus the eval file that
  backs it.
- Grading is **automatic and from disk** — the runner executes the real
  tests against the run tree; an agent's self-report is never the grade
  (ledger S6b and the W3 T1 escape are the standing counterexamples).
- Writing a verdict into the ledger is **agent-run**: same change as the
  results file, per the ledger's own "How a verdict changes" protocol.
  Thresholds are pre-registered before runs (see
  `evals/results/2026-09-30-P2-realcode-prereg.md`).

## 4. Improve — fix in canonical, re-verify

```bash
# 1. edit the capability in canonical/ (never edit adapter output)
# 2. re-render both tools
./scripts/install.sh
# 3. re-run the eval that backs the claim
./scripts/run-eval.sh --task evals/tasks-packaged/<task-id> --tool claude
# 4. update docs/claims-ledger.md + the claim's wiki note in the same change
```

**Agent-run**; steps 2–3 are single commands. A REFUTED claim drives a
fix or a removal — it is not edited into a pass.

## 5. Run an eval — the packaged runner

One entry point: `scripts/run-eval.sh`. It generalizes the Phase 2 W3
runner (`evals/results/2026-09-30-P2-realcode-ab.md`) from scratch code
into a shipped tool.

```bash
./scripts/run-eval.sh --task evals/tasks-packaged/nx-t2-spanning-tree-iterator --tool claude
./scripts/run-eval.sh --task evals/tasks-packaged/nx-t2-spanning-tree-iterator --tool copilot
./scripts/run-eval.sh --task evals/tasks-packaged/<id> --tool claude --arm agent --agent backend
./scripts/run-eval.sh --task evals/tasks-packaged/<id> --tool claude --arm orient --orient <file>
```

- **Task package** (`evals/tasks-packaged/<id>/`): `task.json` (claim
  under test, source repo, parent + fix commits, grading test files and
  pytest nodes, model, timeout), `prompt.txt` (`{PYTHON}` is substituted
  with the grading interpreter), `requirements.txt` (grading env).
- **What a run does:** exports the parent commit (`git archive`) into a
  fresh tree with a fresh single-commit `git init` — no future history,
  the real fix is unreachable from inside the run — runs the tool
  headlessly, overlays the fix commit's test files, executes the grading
  nodes itself, and writes `evals/results/<date>-RUN-<id>-<tool>-<arm>.md`
  with success, turns, cost, wall time, diff stat, and a verdict line.
  Exit codes: 0 PASS, 1 FAIL, 2 harness ERROR (no verdict).
- **Source:** first run clones `source.repo` into
  `evals/scratch-run-eval/cache/` (a full NetworkX clone measured
  3m50s on this connection — one-time); `--source <clone>` or
  `EVAL_SOURCE_DIR` points at an existing clone instead. The source
  clone must be clean; the runner refuses a dirty one.
- **Grading env:** `--python` / `EVAL_PYTHON` wins; else system
  `python3` if pytest imports; else a venv bootstrapped from the task's
  `requirements.txt` under `evals/scratch-run-eval/venv/`.
- **Cost basis:** Claude runs are metered exactly (JSON envelope).
  Copilot runs convert footer tokens at $1/M input, $5/M output with
  cached input at full rate — an upper bound, labeled as such in every
  results file.
- **Arms:** `base` (default); `agent` = a canonical agent installed
  into the run tree (Claude; Copilot's proven path is delegation, not
  packaged here); `orient` = an orientation file placed as `CLAUDE.md`.

### Proof run (this branch, 2026-09-30)

### Proof run (this branch, 2026-09-30)

The proof run pointed `--source` and `EVAL_PYTHON` at the Phase 2 W3
mining clone and its pinned venv (the fastest honest path); the
auto-clone and venv-bootstrap defaults are implemented but were not
exercised by this run — first adopter run pays the clone once.

```bash
EVAL_PYTHON=/home/hatch/workspace/p2/w3/scratch/venv/bin/python \
./scripts/run-eval.sh \
  --task evals/tasks-packaged/nx-t2-spanning-tree-iterator \
  --tool claude \
  --source /home/hatch/workspace/p2/w3/scratch/.infra/nx-src
```

Result (`evals/results/2026-09-30-RUN-nx-t2-spanning-tree-iterator-claude-base.md`):

**VERDICT: PASS — grading tests pass on disk (1/1 nodes).** 11 turns,
$0.103 metered (Claude JSON envelope), 151 s wall. The agent's fix —
initialize the iterator lazily in `__next__` when `partition_queue` is
missing, 1 file, +3 lines — was graded by overlaying the real fix
commit's test file and executing the grading node with the pinned
venv; the agent's own "all tests pass" summary was not consulted.
Ledger claim S17 records this verdict. Total spend for this workstream:
$0.103 of the $2 cap.

## Cadence — the honest table

| Step | Mechanism | Label |
|---|---|---|
| Session record | agent writes it during the session | agent-run |
| Failure hook → `events.jsonl` | tool hook events (Claude proven; Copilot partial) | automatic (partial) |
| OTel file export | env configured once | automatic once enabled |
| Session-harden at close | skill invoked by name | agent-run |
| Eval run | `scripts/run-eval.sh`, one command | agent-run |
| Verdict → ledger | edited with the results file | agent-run |
| Canonical fix + reinstall | edit + `./scripts/install.sh` | manual / agent-run |
| Scheduling (cron / CI) | none shipped | manual — deliberately |

## Not shipped — do not claim these

- No scheduler or CI wiring for evals; no automatic ledger writer.
- No telemetry collector, trace DB, or dashboard — files are the store.
- No Copilot shell-failure hook adapter (identified in E4, not built).
- Session-end auto-invocation of session-harden on Copilot: UNVERIFIED.
- The packaged runner ships with one task package. Packaging a new task
  means mining a real fix commit and oracle-validating it (tests fail
  at the parent, pass at the fix) — the W3 method, done by hand.
