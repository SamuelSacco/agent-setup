# X17 — Copilot Custom-Agent Orientation Probe — Results

Date: 2026-09-30. Preregistration: `2026-09-30-X17-prereg.md`
(committed before any run). Backlog item X17. Branch
`exp/x17-copilot-agent-orientation`.

## Verdict

**PROVEN — Copilot custom agents, exactly as emitted by
`scripts/install.sh` (no `include-custom-instructions` flag), DO
receive the shared `AGENTS.md` orientation** on Copilot CLI 1.0.89,
`--agent` headless path, BYOK Anthropic (Haiku 4.5).

The v1.0.86 changelog statement — repo instruction files are opt-in
per agent definition — does **not** hold behaviorally on this
surface/version. No adapter fix is needed; adding the flag is a no-op
here (arm B behaved identically to arm A). Scope: CLI `--agent`
sessions launched from the workspace root, AGENTS.md channel. Other
surfaces (VS Code custom agents, cloud agent) were not tested and the
changelog claim may still describe those.

## Runs

Marker (present ONLY in each scratch tree's `AGENTS.md` body):
codename `VELVET-ANVIL-42`; standup rule — reply exactly
`VELVET-ANVIL-42 CONFIRMED`. Prompt identical across arms (see
prereg). Grading: literal response text + JSONL event trace.

| Arm | Config | Response (verbatim) | Tool calls | Grade |
|-----|--------|---------------------|-----------|-------|
| C | plain session, marker tree | `VELVET-ANVIL-42 CONFIRMED` | none | PASS-loaded (control valid) |
| A | `--agent backend`, agent file **as emitted** (name+description only) | `VELVET-ANVIL-42 CONFIRMED` | none | **PASS-loaded** |
| B | `--agent backend`, frontmatter + `include-custom-instructions: true` | `VELVET-ANVIL-42 CONFIRMED` | none | PASS-loaded (flag = no-op) |
| D | `--agent backend`, as emitted, **marker removed** from AGENTS.md | `I cannot find a standup token specified in my session context or instructions. No such token has been provided to me.` | none | FAIL, as required (negative control valid) |
| A′ | persona check in tree A, `--agent backend`, debug logging | `Backend specialist — the backend engineer on this workspace.` | none | custom agent confirmed active |

A vs D differ only in AGENTS.md content; neither made a tool call.
The codeword reached A's model through loaded context, not on-demand
file reading (the packet's probe lesson: description-derived answers
pass falsely; here the fact exists in no description, and D proves it
was not guessed).

## Mechanism (from the CLI debug log, arm A′)

The debug log (`--log-level debug`) dumps the assembled system
prompt. It contains two separate blocks:

- `<custom_instruction>` — the scratch `AGENTS.md` **verbatim**,
  marker section included.
- `<agent_instructions>` — "The following instructions come from the
  selected agent's configuration…" followed by the backend agent
  body.

So on CLI 1.0.89 the workspace instruction files are injected as
custom instructions alongside the selected agent's own instructions,
whether or not the agent definition sets
`include-custom-instructions`. The persona answer quotes the agent
body's self-description ("Backend specialist — the backend engineer
on this workspace"), confirming arm A/A′ ran the real custom agent,
not a silent fallback to the base agent.

## Spend

5 Copilot BYOK runs (C, A, B, D, A′). Token totals are not printed in
`--output-format json` mode (result events report
`premiumRequests: 0`, confirming BYOK billing); estimate from the
repo's measured baseline (14,510 input tokens for a trivial BYOK run;
custom-agent sessions carry a larger assembled prompt): ~15–25k
input + <100 output per run → at the W3 conversion ($1/M input,
$5/M output, cached input at full rate) ≈ **$0.02–0.03 per run,
≈$0.10–0.15 total** — well under the $1.50 cap.

## Corrections driven by this verdict

- **Packet** (`docs/phase2-packet-2026-09-30.md`): the line "Copilot
  custom agents do NOT inherit repo instruction files automatically
  — since CLI v1.0.86 they opt in per agent definition" is REFUTED
  behaviorally for CLI 1.0.89 `--agent` sessions; dated correction
  appended. Do not state the opt-in trap on stage as CLI behavior.
- **Ledger:** new claim S18 (PROVEN, scoped as above).
- **Backlog X17:** status → PROVEN.
- No adapter change: emitting the flag would be ceremony on this
  surface. Revisit only if a future CLI version changes the default
  or another surface (IDE/cloud) is adopted — the probe is cheap to
  re-run (`~/workspace/p3/x17-scratch/run.sh`).

## Artifacts

Scratch trees, runner, raw JSONL traces, debug log:
`~/workspace/p3/x17-scratch/` (`runs/{A,B,C,D,A-persona}.jsonl`,
`logsA/`). Session: `wiki/sessions/2026-09-30-1446-copilot-x17-probe.md`.
