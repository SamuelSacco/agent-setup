# X7 Kill Test — planner — Pre-Registration

Written and committed BEFORE any agent eval run. Date: 2026-10-01.
Backlog item X7 (`docs/experiments-backlog.md`): planner /
code-explorer provisional roster entries earn their place. This file
covers **planner only** (code-explorer is a separate worker, branch
`wave2c/x7-code-explorer-kill-test`, prereg
`evals/results/2026-10-01-X7-code-explorer-prereg.md` at `1228f44`;
this file mirrors its structure and discipline).
Branch: `wave2c/x7-planner-kill-test` off master `e181f61`.

## Claim under test

"planner (canonical specialist, read/search only) earns its roster
place: on implementation-planning tasks it beats or matches the
base tool at no higher cost."

## Why the task type differs from S11 (recorded pre-run)

X7's cheapest-test line says "S11-protocol A/B". S11 graded
write/bugfix tasks by overlaying fix-commit tests. planner as
emitted (`.claude/agents/planner.md`) carries
`tools: [Read, Grep, Glob]` — it cannot write a fix, so a
write-graded A/B would fail the agent arm by construction and
would measure the tool restriction, not planning quality.
Adaptation, decided pre-run: keep the S11 skeleton (4 paired
tasks, identical prompts, identical CLI flags, one variable =
`--agent`, discordant-pair rule, X7 kill rule verbatim, grading
from disk only) and change only the task class to the agent's
target class — implementation planning on a small codebase, the
work its canonical definition specifies (requirements analysis,
architecture review, step breakdown with file paths / dependency
order / risks). Grading artifacts are the evaluator-saved run
envelopes/result texts on disk, scored by the evaluator against
the fixed answer key below; agent self-report is never the grade
(the saved result text is the deliverable under test).

## Fixtures

Four small self-contained Python codebases, committed with this
prereg under `evals/fixtures/x7-planner/` (67–86 lines of app code
each). Each embeds at least one convention/trap that a correct plan
must respect and that is discoverable only by reading the code:

- `p1-stockalert/` — Stockroom inventory service.
- `p2-reset/` — Passkeep user-account service.
- `p3-schedpub/` — Pressroom blog engine.
- `p4-retry/` — Payloop payment service.

Evaluator verification pre-run: all app/test files compile
(`py_compile` OK) and all 8 fixture tests pass (direct invocation;
pytest is not installed in this sandbox).

Each run gets a fresh copy of exactly one fixture (plus the arm
setup below), fresh single-commit `git init`.

## Tasks (4) and answer key (evaluator-derived from disk, pre-run)

Each task: identical prompt to both arms (full text in the runner,
`~/workspace/w2c-x7-planner-scratch/runner.py`, frozen at prereg
commit). Each prompt asks for an implementation plan only — no
code changes — naming exact files/functions, dependency order,
and risks. Each is scored on 5 checks (regex groups over the saved
result text, case-insensitive; any pattern in a group scores it).
Task PASS = ≥4/5 checks AND no fabrication (below).

- **PL1 — low-stock alert (p1-stockalert).** Feature: when an order
  causes a SKU's on-hand stock to reach or fall below its reorder
  point, send one alert email to the ops address; alert only on
  the crossing, not on every later order while stock stays low.
  Checks: (1) hook point: `adjust_stock`;
  (2) threshold source: `reorder_point`;
  (3) outbound path reuse: `send_email`;
  (4) recipient source: `ALERT_EMAIL`;
  (5) crossing-only semantics: `cross` / `was above` /
  `before (the )?(adjustment|change|decrement)` / `transition`.
  Ground truth: `app/inventory.py:adjust_stock` is the only stock
  mutation point (`app/orders.py:create_order` calls it);
  `StockLevel.reorder_point` at `app/models.py:13`;
  `app/alerts.py:send_email` is the single outbound-email path;
  `ALERT_EMAIL` at `app/config.py:1`. Trap: routing through
  `app/scheduler.py` daily jobs contradicts the crossing spec.
- **PL2 — password reset (p2-reset).** Feature: a user requests a
  reset by email, receives a reset link built on the app's base
  URL carrying a token that expires; submitting a valid token
  sets the new password and signs the user out everywhere.
  Checks: (1) user lookup + password set: `set_password`;
  (2) mail path reuse: `send_email`;
  (3) token storage rule: `hash_token`;
  (4) session invalidation: `invalidate_sessions_for`;
  (5) link/expiry mechanism: `BASE_URL` or `expir` / `TTL`.
  Ground truth: `app/users.py:set_password` + `get_user_by_email`
  (users live in `users.py`'s own dict — `app/db.py` is an unused
  stand-in); `app/emailer.py:send_email`; `app/security.py`
  convention: bearer/reset tokens are stored ONLY as SHA-256
  hashes via `hash_token()` — a plan persisting the raw token
  misses check 3; `app/auth.py:invalidate_sessions_for`;
  `BASE_URL` at `app/config.py:2`. Trap: OAuth users
  (`app/oauth.py`) have no local password.
- **PL3 — scheduled publishing (p3-schedpub).** Feature: an author
  sets a future publish time on a draft; the post goes live
  automatically at that time and then appears in the RSS feed.
  Checks: (1) publish transition reuse: `publish(` or
  `posts.publish` or `` `publish` ``;
  (2) schedule stored on the post: `scheduled` (e.g.
  `scheduled_at`);
  (3) periodic driver: `add_job` / `run_pending`;
  (4) time convention: `now_utc` / timezone-aware UTC;
  (5) feed visibility path: `list_published`.
  Ground truth: `app/posts.py:publish` performs the one-way
  draft→published transition and stamps `published_at`;
  `app/jobs.py:run_pending` is called once per minute by the
  worker; `app/timeutil.py` convention: all stored timestamps are
  timezone-aware UTC from `now_utc()` (2026-07 incident from naive
  local times); `app/feeds.py:rss_items` reads via
  `list_published()`, so a published post reaches RSS with no
  feed change.
- **PL4 — automatic retry of failed charges (p4-retry).** Feature:
  a failed charge is retried automatically, up to the configured
  attempts with the configured delays between attempts, and a
  retry must never double-charge the customer.
  Checks: (1) retry location: `worker` + (`enqueue` /
  `process_queue`);
  (2) delay source: `BACKOFF_SECONDS`;
  (3) no-double-charge mechanism: `idempotency` + (`same` /
  `reuse` / `original`);
  (4) retried call: `charge(`;
  (5) failed-only guard: `failed` near `status` / `only` near
  `failed` (regex proximity, either order, ≤40 chars).
  Ground truth: `app/worker.py` is the ONLY place repeated work
  runs (worker policy comment, 2026-08 review) and defines
  `BACKOFF_SECONDS = [60, 300, 1800]`; `app/billing.py:charge` is
  idempotent — a repeat call with the same `idempotency_key`
  returns the original `Payment` and does not charge again;
  `app/api.py:post_charge` must stay a single synchronous
  `charge()` call (no inline retry).

- **Fabrication check (all tasks):** every `.py` path cited in
  the result text (backticked or bare token ending `.py`) must
  exist in that task's fixture tree. Any cited path that does not
  exist = fabrication = task FAIL regardless of checks. (A path
  token is checked after stripping punctuation; tokens containing
  `*` are skipped as globs.)

## Arms

Same for every run: Claude Code 2.1.285 headless,
`claude -p '<prompt>' --model claude-haiku-4-5-20251001
--output-format json --permission-mode acceptEdits
--allowedTools 'Read Grep Glob Bash'`, scratch
`.claude/settings.json` = `{"apiKeyHelper": <vault helper>}`,
per-run wall cap 600 s. (No Write/Edit in either arm: the task is
plan-only; this also keeps the base arm from being graded on
edits. This is the one flag difference from S11, forced by the
task class and applied identically to both arms.)

- **Arm 1 — base:** fresh fixture copy + settings.json only.
- **Arm 2 — +agent (planner):** identical + the emitted agent
  file `.claude/agents/planner.md` from master `e181f61`
  (adapter output, `tools: [Read, Grep, Glob]`) copied into the
  run tree's `.claude/agents/`; run adds `--agent planner`.

Run order: PL1 base, PL1 agent, PL2 base, PL2 agent, PL3 base,
PL3 agent, PL4 base, PL4 agent (pairs adjacent, base first —
same order bias for every pair, recorded).

## Metrics

Per run: task PASS/FAIL (primary), checks hit (x/5), fabrication
flag, `num_turns` + `total_cost_usd` from the JSON envelope,
wall seconds. Per arm: tasks passed, total cost, total turns.

## Verdict rule (X7 kill rule, pre-registered)

Claim = "planner earns its place".

- **PROVEN** (keep): agent passes ≥1 task base fails (discordant
  win) AND agent total passes ≥ base total passes.
- **REFUTED** (kill): agent passes fewer tasks than base, OR
  (no discordant win AND agent total cost ≥ base total cost) —
  the backlog X7 kill condition verbatim.
- **UNVERIFIABLE**: any other outcome (equal passes, no discordant
  win, agent cheaper; or incomplete pairs / harness errors).

Secondary, descriptive only: mean checks per task per arm; cost
and turn totals. No threshold on secondaries.

## Budget and stop rules

- Hard cap: $2.00 metered (Claude JSON envelopes) for this item.
- Single-run soft cap $0.60: a run passing it is killed and
  logged; its pair is incomplete → UNVERIFIABLE path unless the
  remaining pairs already decide the verdict under the rule above.
- No run starts if cumulative spend + $0.60 would exceed $2.00.
- Rigor (fresh tree per run, identical prompts, disk grading) is
  never shrunk.

## Artifacts

- Runner + prompts + raw envelopes + per-run grades:
  `~/workspace/w2c-x7-planner-scratch/` (`runner.py`, `grade.py`,
  `runs/`, `ledger.tsv`, `grades.json`).
- Results: `evals/results/2026-10-01-X7-planner-results.md`.
- Ledger: S11 scope note in `docs/claims-ledger.md` (planner
  result, this protocol); backlog X7 updated in
  `docs/experiments-backlog.md` (planner half only; code-explorer
  half is the sibling worker's).
