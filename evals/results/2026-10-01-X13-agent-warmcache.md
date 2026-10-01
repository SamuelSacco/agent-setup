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

_(filled after the run)_

## Timed runs

_(filled after the runs)_

## Verdicts

_(filled after grading)_
