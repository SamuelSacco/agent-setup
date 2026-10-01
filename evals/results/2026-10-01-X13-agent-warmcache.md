# X13 — Copilot `--agent` Marker Invocation, 3 More Agents, Warm MCP Cache

## Pre-registration (written and committed BEFORE any probe run)

Date: 2026-10-01. Backlog item X13. Ledger claim S15. Branch
`lab/x13-agent-warmcache`.

### Question

Ledger S15: Copilot `--agent <name>` headless is PROVEN for
`code-reviewer` only (201 s, 110,590 input tokens, full tree). A second
attempt in a minimal tree stalled in MCP startup (cold npx cache) and
was killed at 300 s. The other 11 agents are UNVERIFIABLE on this path.
X13 tests whether 3 more canonical agents complete via `--agent` when
the MCP cache is warm.

### Agents under test (fixed in advance)

| Agent | Class | Persona check (fact present only in that agent's emitted body) |
|---|---|---|
| planner | read-only (`tools: [read, search]`) | Worked example in its Plan Format section: a Stripe subscription billing plan. Expected keywords: `Stripe`, `subscription` |
| security-reviewer | review (`tools: [read, shell, search]`) | Pattern table row for string-concatenated SQL. Expected: severity `CRITICAL`, fix `parameterized` |
| backend | edit (`tools: [read, edit, shell, search]`) | Working rule: state the contract before implementing it. Expected keywords: `contract`, `inputs`/`outputs`/`failure modes` |

Agent files: byte-identical copies of the files `scripts/install.sh`
emits into `.github/agents/` (installer re-run in this clone before
the probe; tree converged, no diff).

### Scratch tree

`~/workspace/w4c-x13-scratch/tree/` (git-initialised, one commit):

- `AGENTS.md` — short orientation file carrying ONE marker fact that
  exists nowhere else in the tree, the agent files, or the prompt:
  release-train codename `COPPER-FALCON-73`; standup rule — reply
  exactly `COPPER-FALCON-73 CONFIRMED`.
- `.github/muse-instructions.md` — byte-identical copy of the
  emitted file (no marker facts).
- `.github/agents/{planner,security-reviewer,backend}.agent.md` —
  byte-identical emitted files.
- `.github/mcp.json` — byte-identical emitted file, kept in place for
  all runs (the warm-cache arm's point; S15's stall was cold-cache).
  A minimal `wiki/` directory is present so the emitted
  filesystem-wiki server's `./wiki` argument resolves.
- No `CLAUDE.md`.

### Warm-up (fixed in advance)

One plain session (no `--agent`) in the same scratch tree, trivial
prompt (`Reply with exactly: warm`), same BYOK configuration, timeout
300 s, BEFORE the timed runs. Its cost and wall time are recorded
separately and do not count toward any agent verdict. Purpose: hot
npx MCP cache in the real HOME shared by all subsequent runs.

### Timed runs

Tool: Copilot CLI 1.0.89 (`~/workspace/tools/bin/copilot`), BYOK
Anthropic (provider `anthropic`, base URL api.anthropic.com, model
`claude-haiku-4-5-20251001`, key via the vault helper, never printed),
`COPILOT_ALLOW_ALL=true`, `--allow-all-tools --allow-all-paths`,
`--output-format json`. One run per agent, sequential, timeout 300 s
each; a stalled run is killed at 300 s and recorded as a stall, not
retried.

Prompt (identical except Part 2, per agent):

> Workspace check — answer from your session context only; do not
> read any files or run any commands. Part 1: What is this
> workspace's standup token? Reply with exactly the token as
> specified in your instructions. Part 2: <persona question>.
> Answer both parts, labelled `Part 1:` and `Part 2:`.

Persona questions:

- planner: "According to your own instructions, what worked example
  plan do you carry, and what payment provider and product does it
  use?"
- security-reviewer: "According to your own code-pattern table, what
  severity and what fix do you assign to string-concatenated SQL?"
- backend: "According to your own working rules, what must you state
  before implementing a change, and what does it consist of?"

### Grading (from literal output + event trace, never self-report)

- Check 1 (orientation): response text contains
  `COPPER-FALCON-73 CONFIRMED`.
- Check 2 (persona): response text contains the agent's expected
  keywords from the table above.
- Both checks FAIL if the JSONL event stream shows any tool call: the
  facts must come from loaded context (orientation block + agent
  instructions), not on-demand file reading (X17 grading rule).

### Decision rule (fixed in advance)

- Per agent **PROVEN**: run completes (result event, exit 0) within
  300 s with both checks PASS.
- Per agent **REFUTED**: run errors or stalls in a way attributable
  to the `--agent` path itself.
- Per agent **UNVERIFIABLE**: failure attributable to unrelated
  infrastructure (named explicitly).
- Overall X13 verdict aggregates the three per-agent verdicts.

### Budget

Cap ~$2.50 converted (batch cap $5). Conversion: repo convention —
token totals at $1/M input, $5/M output, cached input at full rate
(upper bound). Reference: S15's completed `--agent` run metered
110,590 input tokens (~$0.11); 1 warm-up + 3 timed runs project
~$0.50.

## Warm-up record

One plain session (no `--agent`), prompt `Reply with exactly: warm`,
same tree and BYOK configuration, run before the timed runs.

- Result: exit 0, wall 186 s, response verbatim: `warm`.
- Event trace: all 5 workspace MCP servers went `pending` in parallel
  at startup; playwright connected at ~16 s, sequential-thinking at
  ~30 s; github, context7, filesystem-wiki each FAILED with "MCP
  lifecycle negotiation did not complete within 60000 ms"; a
  user-scope `github-mcp-server` then connected. Session proceeded:
  `session.mcp_servers_loaded` at ~117 s, first model answer at
  ~170 s session time after 3 transport-failure retries (10 s each).
- Cost: `premiumRequests: 0` (BYOK). Token totals are not printed in
  `--output-format json` mode; X17 baseline conversion gives
  ~$0.02–0.03 for this run.
- Note: the warm-up proves the cache was hot and a plain session in
  this exact tree completes — and that even warm, 3 of 5 emitted MCP
  servers fail the 60 s lifecycle cap in this environment.

## Timed runs

All three runs: exit 124 (killed by the 300 s probe timeout), no
`result` event, no `user.message` event, zero model calls, zero tool
calls. stderr (all three, identical): `Error executing prompt: Error:
Cannot invoke native session after disposal has started` (emitted at
kill time).

| Agent | Wall | Bytes | Response | Check 1 (marker) | Check 2 (persona) | Grade |
|---|---|---|---|---|---|---|
| planner | 300 s (killed) | 3,516 | none — never reached the prompt | FAIL | FAIL | STALL |
| security-reviewer | 300 s (killed) | 3,934 | none — never reached the prompt | FAIL | FAIL | STALL |
| backend | 300 s (killed) | 3,514 | none — never reached the prompt | FAIL | FAIL | STALL |

### Stall mechanism (from the event traces, all three runs)

MCP startup on the `--agent` path is SERIALIZED, unlike the plain
session. Per run, the trace shows one server `pending` at a time:

1. `context7` pending → failed at ~65 s (60 s lifecycle cap).
2. `filesystem-wiki` pending → failed at ~65 s.
3. `github` pending → failed at ~65 s.
4. `github-mcp-server` pending, then a SECOND pass begins: context7,
   filesystem-wiki, github, playwright, sequential-thinking all
   `pending` again — still unresolved when the 300 s kill lands.

The session never emits `session.mcp_servers_loaded`, so the prompt
is never delivered. Contrast, same tree / same HOME / minutes
earlier: the plain warm-up session started all 5 servers in parallel
and proceeded past MCP loading at ~117 s despite the same 60 s
lifecycle failures. Warming the npx cache did not change the outcome:
the lifecycle failures occurred in the warm-up too, and on the
`--agent` path their serialized cost (≥5 × ~65 s, plus a second pass)
exceeds the 300 s budget by construction.

This is the S15 cold-cache fragility in a stronger form: the failure
is not cold-cache-specific. With the emitted `.github/mcp.json` in
place, `--agent` sessions serialize MCP initialization, and any
server that hits the 60 s lifecycle cap makes a 300 s completion
near-impossible when several servers fail.

## Verdicts

Per-agent, under the pre-registered decision rule (stall attributable
to the `--agent` path — serialized MCP startup is a property of that
path, proven by the parallel-start plain-session control in the
identical tree):

- planner: **REFUTED** on this path/configuration (300 s stall, no
  model call).
- security-reviewer: **REFUTED** on this path/configuration (300 s
  stall, no model call).
- backend: **REFUTED** on this path/configuration (300 s stall, no
  model call).

**Overall X13: REFUTED** — with a warm MCP cache and the emitted MCP
config in place, 0 of 3 additional canonical agents completed via
`copilot --agent <name>` within 300 s. Scope: Copilot CLI 1.0.89,
BYOK Haiku 4.5, minimal scratch tree carrying the emitted
`.github/mcp.json` (5 servers). This does not refute the agent files
or personas (no run reached a model call; S14 delegation proves all
12 invocable) and does not overturn S15's `code-reviewer` completion
(full repo tree, 201 s). It refutes the expectation that a warm cache
makes the `--agent` path generally usable: the binding constraint is
serialized MCP startup × the 60 s lifecycle cap, not cache warmth.

Cheapest follow-up (not run, out of scope/budget): repeat one agent
with `.github/mcp.json` removed (the X17 configuration, which
completed quickly for backend via the orientation probe) to isolate
MCP config presence as the trigger.

## Spend

4 Copilot BYOK runs total (1 warm-up + 3 timed). Timed runs made zero
model calls: $0. Warm-up: ~$0.02–0.03 converted (X17 baseline;
`premiumRequests: 0`, token totals not emitted in json mode).
**Total ≈ $0.03** — under the ~$2.50 cap.

## Artifacts

Scratch tree, runner, raw JSONL traces + stderr:
`~/workspace/w4c-x13-scratch/` (`tree/`, `run.sh`,
`runs/{warmup,planner,security-reviewer,backend}.{jsonl,stderr}`).

