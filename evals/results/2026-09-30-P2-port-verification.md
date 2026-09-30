# P2 Port Verification — 2026-09-30

Workstream: Phase 2 follow-up. Tools: Claude Code 2.1.285 (`~/workspace/tools/bin/claude`),
Copilot CLI 1.0.89 (`~/workspace/tools/bin/copilot`), both on `claude-haiku-4-5-20251001` via the
stored Anthropic key (Claude: apiKeyHelper; Copilot: BYOK env) — S7 setup, model constant.

Question: W2 ported 19 ECC items into `canonical/` (9 agents, 6 skills, 4 MCP) and `install.sh`
emits them, but no live invocation probe had run. This eval verifies the full emitted set —
12 agents, 8 skills (6 ports + session-harden + wiki-lint), 5 MCP servers (4 ports +
filesystem-wiki) — per port × per tool. File presence is not evidence: every verdict below
rests on an invocation marker, a tool-call event, or a captured tool result.

Method: scratch copy of the phase-2 tree (`git archive`), `scripts/install.sh` run in the copy,
isolated `HOME` per case. Agent probes ran the session AS the agent (Claude `--agent <name>`;
Copilot negative control `--agent`, working path = task-tool delegation) with a marker task:
read `probe-input.txt` (token `PV-TOKEN-7F3A`, never in the prompt), write
`probe-out/<tool>-agent-<name>.txt` containing `<name> <token>`. Skill probes invoked each
skill by name (Claude: Skill tool, stream-json; Copilot: skill tool + session-state events).
MCP probes ran at three levels: raw JSON-RPC against the emitted `.mcp.json` (initialize,
tools/list, one trivial tools/call), `mcp list` in each CLI, and one model-mediated call per
server per tool. Probe scripts: `evals/fixtures/p2-port-verification/`.

## Agents (12)

Discovery, both tools, $0: a bogus `--agent pv-bogus-nonexistent` is refused pre-flight by both
CLIs, and each refusal lists exactly the 12 canonical agents (Claude adds its built-ins).

| Agent | Claude (`--agent`) | Copilot (task delegation) |
|---|---|---|
| backend | PROVEN — marker, $0.0162 | PROVEN — marker |
| build-error-resolver | PROVEN — marker, $0.0177 | PROVEN — marker |
| code-architect | PROVEN — marker, $0.0169 | PROVEN — marker |
| code-explorer | PROVEN — marker, $0.0168 | PROVEN — marker |
| code-reviewer | PROVEN — marker, $0.0342 | PROVEN — marker (delegation; see --agent finding) |
| data-scientist | PROVEN — marker, $0.0166 | PROVEN — marker |
| doc-updater | PROVEN — marker, $0.0173 | PROVEN — marker |
| planner | PROVEN — marker, $0.0185 | PROVEN — marker |
| refactor-cleaner | PROVEN — marker, $0.0175 | PROVEN — marker |
| security-reviewer | PROVEN — marker, $0.0180 | PROVEN — marker |
| tdd-guide | PROVEN — marker, $0.0170 | PROVEN — marker |
| ux-ui | PROVEN — marker, $0.0159 | PROVEN — marker |

All 24 marker files verified verbatim (`<name> PV-TOKEN-7F3A`). Claude runs: 3 turns each.

**Copilot `--agent` finding (path-level, not per-port):** running the session AS the ported
`code-reviewer` never completed the trivial marker task — attempt 1 (full repo tree) hit the
600 s timeout, attempt 2 (minimal tree, "do not review" prompt) hit 300 s; no marker either
time; ~442k and ~97k session input tokens respectively (upper-bound accounting below). The
persona's review process drives open-ended exploration with no stop. For the other 11 agents
the `--agent` path is UNVERIFIABLE (not retried — the delegation path is proven and cheaper).
Verdict for the path with these personas, headless: REFUTED on the one agent tested.

## Skills (8)

| Skill | Claude (Skill tool) | Copilot (skill tool) |
|---|---|---|
| architecture-decision-records | PROVEN | PROVEN |
| codebase-onboarding | PROVEN | PROVEN |
| documentation-lookup | PROVEN | PROVEN |
| search-first | PROVEN | PROVEN |
| session-harden | PROVEN | PROVEN |
| tdd-workflow | PROVEN | PROVEN |
| verification-loop | PROVEN | PROVEN |
| wiki-lint | PROVEN | PROVEN |

Claude evidence: `Skill` tool_use events naming each skill in stream-json, paired runs,
$0.079 total. Copilot evidence: `skill` tool executions naming each skill in the stdout event
stream (all 8), plus `skill.invoked` session-state events for 6 of 8 — in two pairs only the
second skill emitted `skill.invoked` (context-delivery dedup in the session log; the tool
execution events cover all 8). Prompts instructed load-and-stop, so this proves discovery +
invocation, not full workflow completion.

## MCP servers (5)

| Server | Protocol (JSON-RPC) | Claude call | Copilot call |
|---|---|---|---|
| context7 | PROVEN — 2 tools; `resolve-library-id` → `/reactjs/react.dev` | PROVEN | PROVEN |
| sequential-thinking | PROVEN — 1 tool; thought recorded | PROVEN | PROVEN (warm cache; see finding) |
| filesystem-wiki | PROVEN — 14 tools; `list_directory` listed the wiki | PROVEN | PROVEN (warm cache; see finding) |
| github | PROVEN — 26 tools; `search_repositories` returned 442,496 results | PROVEN | PROVEN |
| playwright | PARTIAL — 25 tools listed; call REFUTED as-shipped in this sandbox, PROVEN with `--no-sandbox` (scratch config only) | REFUTED (sandbox) | REFUTED (sandbox) |

Notes per server:

- **github**: works *unauthenticated* for public search despite the port shipping
  `GITHUB_PERSONAL_ACCESS_TOKEN: ""`. Authenticated operations remain UNVERIFIABLE (no token
  was set; by design — the canonical file says "set the env token before use").
- **playwright**: failure is environmental, stacked: (1) no Chrome in the sandbox — after
  `npx playwright install chrome` (sandbox provisioning, canonical untouched) the error became
  (2) Chromium refuses to run as root without `--no-sandbox`. With `--no-sandbox` appended in a
  scratch config, `browser_navigate about:blank` succeeds at protocol level. On a non-root
  developer machine the as-shipped config is UNVERIFIABLE from here. The port content is ECC
  verbatim; it was not modified.
- **filesystem-wiki**: the server resolves tool paths against its allowed root (the `./wiki`
  arg). `list_directory` with `./wiki` double-resolves to `wiki/wiki` (ENOENT); absolute path
  or `.` works. The server also exits at startup if `./wiki` does not exist relative to its
  cwd — Copilot probes in a wiki-less minimal tree failed for this reason alone; the passing
  probes ran in the full tree.
- **context7**: current server (v4.1.1) validates `resolve-library-id` arguments strictly —
  both `query` and `libraryName` are required; either alone returns a validation error. Not a
  port defect; recorded for the next person who writes a probe.

**Copilot MCP cold-cache finding:** with a fresh `HOME` (empty npx cache), Copilot spawns all
workspace servers in parallel and cold downloads race its 60 s lifecycle-negotiation cap:
first combined run — sequential-thinking and filesystem-wiki died with Node ESM loader errors,
context7 connected at ~51 s; second run (another fresh HOME) — both failed at the 60 s cap.
After warming the npx cache in that HOME (one sequential protocol pass), both connected in
seconds and answered calls. Claude Code showed no equivalent failure (its startup tolerates
the same cold cache). Operational rule: first Copilot run in a fresh environment may need a
retry before MCP verdicts mean anything.

**Adapter verdict:** no adapter-level breakage found. Every emitted file was consumable as
emitted: `.claude/agents/*.md`, `.github/agents/*.agent.md`, both skill trees, root `.mcp.json`
and dual-key `.github/mcp.json` (W1 fix) all functioned. `claude mcp list` reports the five
project servers as "Pending approval" in a fresh HOME (project-scope approval state); headless
runs with the tools allowlisted executed them regardless. `copilot mcp list` lists all five
workspace servers under `COPILOT_ALLOW_ALL=true`.

## Cost log

Budget cap $6.00. **Total: ~$2.78.** Claude costs are exact (`total_cost_usd`). Copilot costs
are session totals from `session.shutdown` `modelMetrics`, converted at flat Haiku rates
($1/M input, $5/M output) — the W1/W3 convention; the input figure includes cache reads, so
Copilot numbers are upper bounds.

| Surface | Runs | Cost |
|---|---|---|
| Claude agents (12× `--agent` + 2 negative controls at $0) | 14 | $0.2226 |
| Claude agents — duplicate partial execution (runtime restart of the batch; 5 runs observed in its output before the clean re-run) | 5 | $0.2780 |
| Claude skills (4 paired runs) | 4 | $0.0789 |
| Claude MCP combined (5 calls in one run) | 1 | $0.0517 |
| Copilot agents (2 `--agent` timeouts, 1 delegation pilot, 6 paired delegation runs) | 9 | ~$1.7556 |
| Copilot MCP (combined + 2 re-probes) | 3 | ~$0.1574 |
| Copilot skills (4 paired runs) | 4 | ~$0.2326 |
| MCP protocol probes, `mcp list`, negative controls | — | $0.0000 |
| **Total** | | **~$2.7768** |

## Caveats

- Invocation probes prove the ports load and execute under instruction; they do not grade
  output quality (that was W3's question for agents, still UNVERIFIABLE there).
- Copilot per-run attribution rests on session shutdown metrics; one batch session's shutdown
  record was not found, so the Copilot agent total is the recorded sum, not a reconstruction.
- The Claude agent batch executed twice (runtime restarted the backgrounded batch; the first
  execution's output showed one 22-turn/$0.149 build-error-resolver run with no marker — the
  clean re-run wrote all markers at 3 turns each). Both executions are charged above.
