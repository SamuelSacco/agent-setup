# Q15 / X13 follow-up — preregistration: isolate serialized MCP startup

Date: 2026-10-01. Parent: X13 (`evals/results/2026-10-01-X13-agent-warmcache.md`,
branch `lab/x13-agent-warmcache`, merged to master as 666944b after this
branch was cut). Ledger claim under test: S15 (amended by X13). Branch
`lab/x13-mcp-isolation` off `e181f61` per tasking (pre-X13-merge master).

## Question

X13 showed `--agent` sessions serialize MCP startup: one server at a
time, each 60 s lifecycle failure costing ~65 s, second pass before the
300 s kill — with zero model calls. Is serialized startup of the
**workspace `.github/mcp.json`** the binding mechanism of those stalls?

## Design (fixed before any run)

- Agent: `planner` — the X13 trace with the cleanest serialization
  signature (context7 65 s → filesystem-wiki 65 s → github 65 s, then a
  second parallel pass that never resolves).
- Arms, identical except one variable:
  - `with`: `.github/mcp.json` present (byte-identical to X13's,
    sha256 `1ff95bb27dc9aee6babc3df04ca2363cc3820b463eca4dade559c8d228a1a54c`).
  - `without`: `.github/mcp.json` REMOVED (the "X17 configuration").
- Trees: `~/workspace/q15-x13-scratch/tree-with/` and
  `.../tree-without/`, copied from the X13 scratch tree (AGENTS.md with
  marker `COPPER-FALCON-73`, `.github/muse-instructions.md`,
  `.github/agents/{planner,security-reviewer,backend}.agent.md`, minimal
  `wiki/index.md`); `diff -r` differs only in `.github/mcp.json`.
- HOME hygiene: each arm runs under a FRESH copy of an empty
  `home-template/` — i.e. no `~/.copilot/mcp-config.json` (the W1
  user-scope install that changed W4 behavior mid-wave) and no other
  copilot state. Workspace file is the only MCP source. HOME contents
  documented per arm.
- Held constant: Copilot CLI binary (1.0.90 — NOTE: X13 used 1.0.89;
  both arms share the newer binary, so the arm comparison is clean;
  drift vs X13 recorded, not corrected), BYOK env
  (`COPILOT_PROVIDER_TYPE=anthropic`, base URL api.anthropic.com, model
  `claude-haiku-4-5-20251001`, key via vault helper, never printed),
  `COPILOT_ALLOW_ALL=true`, flags
  `--output-format json --allow-all-tools --allow-all-paths`,
  `--agent planner`, timeout 300 s, prompt below. npx cache is shared
  and warm (real `~/.npm`, 1.2G) via explicit `NPM_CONFIG_CACHE` so
  cache warmth is a constant, not a per-arm variable. Builtin MCP
  servers are NOT disabled (matches X13; any builtin traffic is
  measured). Arm order fixed: `with` first, then `without`.

## Prompt (identical, X13 planner wording)

> Workspace check — answer from your session context only; do not read
> any files or run any commands. Part 1: What is this workspace's
> standup token? Reply with exactly the token as specified in your
> instructions. Part 2: According to your own instructions, what
> worked example plan do you carry, and what payment provider and
> product does it use? Answer both parts, labelled `Part 1:` and
> `Part 2:`.

## Grading

- Completion marker: a `result` event exists AND response text contains
  `COPPER-FALCON-73 CONFIRMED` (no tool calls, X17 grading rule).
- Persona check: response contains `Stripe` + `subscription`.

## Verdict rule (registered before running)

- **PROVEN (mechanism CONFIRMED)**: `with` reproduces the X13 stall
  signature (serialized server starts in the trace, or
  `session.mcp_servers_loaded` absent / grossly delayed, no model call
  before the 300 s kill) AND `without` reaches model calls and
  completes with the marker within 300 s.
- **REFUTED (mechanism lies elsewhere)**: `without` stalls the same
  way as `with`, OR `with` completes fine (X13 does not reproduce in
  this environment).
- **UNVERIFIABLE**: environment drift blocks a clean comparison —
  named explicitly (candidate known drift: CLI 1.0.89 → 1.0.90; S24
  evidence that workspace MCP scope is dead on 1.0.89, which would make
  both arms behave identically).

## Budget

Hard cap $1 converted total (both arms). Runs are stall-time, not
tokens; a stalled run is killed at the 300 s preregistered timeout, not
before. Conversion: $1/M input, $5/M output (cached input at full
rate); `premiumRequests: 0` (BYOK). Reference: X13 warm-up ~$0.02–0.03.

## Artifacts (in this branch)

`evals/results/2026-10-01-X13-mcp-isolation.md`; runner + raw traces in
`~/workspace/q15-x13-scratch/` (`run.sh`, `runs/{with,without}.{jsonl,stderr}`,
HOME snapshots).
