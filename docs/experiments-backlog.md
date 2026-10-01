# Experiments backlog — triage lab, 2026-09-30

Harvested 2026-09-30 (W2 triage stream, branch `lab/triage`) from
`docs/phase2-packet-2026-09-30.md`, `docs/phase2-addendum-2026-09-30.md`,
`docs/morning-review-2026-09-30.md`, `docs/claims-ledger.md`, `wiki/notes/`,
and `evals/results/`. Every item: the claim in one line, current status, the
cheapest DECISIVE test, estimated cost, priority. Verdicts land here first,
then propagate as dated correction notes — history is never rewritten.

Status key: UNVERIFIABLE / PARTIAL / REFUTED / PROVEN / UNBUILT / BLOCKED.

## Landed this run (2026-09-30, W2)

- **X2 — description-rent figures: REFUTED as stated.** Re-measured from
  `canonical/agents/*.md` frontmatter (tiktoken cl100k): all 12 agents =
  422 tokens description-only, 469 with names — not ~546. Roster-v2 six:
  only five map to files (178 tokens); `task-runner` has no canonical file,
  and even at the max observed per-agent rent (49) the six total 227 — not
  ~300. Direction survives (six ≈ half or less of twelve); the point
  figures do not reproduce under any counting method tried (desc-only 422 /
  name+desc 469 / full frontmatter 739). Side-finding: the packet's rent
  framing omits skills — 8 skill descriptions add 430 tokens.
  Evidence: `evals/results/2026-09-30-LAB-rent-toolcounts.md`.
- **X1a — per-agent tool budgeting is implemented: REFUTED.** Canonical
  agents carry only `tools_hint` (2–4 abstract categories); emitted
  `.claude/agents/*.md` and `.github/agents/*.md` contain zero `tools:`
  restrictions — every agent loads the full session toolset. Measured
  loads: Claude default session 12 tool defs, Copilot default 23 tools
  (OTEL decomposition, ledger S8–S10). Both sit under 35, so the rule is
  vacuously satisfied and enforced by nothing.
  Evidence: `evals/results/2026-09-30-LAB-rent-toolcounts.md`.
- **X15 — run-eval.sh default path: PROVEN.** The S17 carve-out is
  closed: in a clean tree, with no `--source` and no `EVAL_PYTHON`, the
  runner auto-cloned the task source and bootstrapped the grading venv,
  then PASS (1/1 grading nodes, disk-graded), 11 turns, $0.1145 metered,
  exit 0. Ledger S17 amended. Evidence:
  `evals/results/2026-09-30-RUN-nx-t2-spanning-tree-iterator-claude-base-defaultpath.md`.

## Backlog

### X1 — ≤ ~35 loaded tools per agent before splitting into subagents
- Status: UNVERIFIABLE folklore (threshold); implementation REFUTED (X1a).
- Cheapest decisive test: A/B on 4 mined real-code tasks, agent with full
  toolset vs same agent restricted to ≤12 concrete tools; discordant-pair
  rule. Nothing in the repo ties "35" to any outcome; treat as a talk
  heuristic, never a finding.
- Est. cost: ~$1.50. Priority: medium (it is in the talk close).

### X2 — Context-rent budget rule uses the packet's rent figures
- Status: figures REFUTED this run (see above); rule itself (fewer defaults
  → ~half the listing rent) consistent with re-measurement.
- Cheapest decisive test: done for agents. Remaining: re-derive the
  "~3.5k for all-68 ECC" figure from the ECC source (not in this repo) or
  retire the number. Est. cost: $0 (web fetch of ECC repo). Priority: high
  — the figure is in the packet the talk is built from.
- **Correction 2026-09-30 (X2 remainder, branch `lab/x2-ecc-rent`):
  remainder CLOSED — "~3.5k" REFUTED as a token figure, retired.**
  Re-derived from the ECC source at the mined commit
  (`affaan-m/ECC` `c70874fae9eb0e5ad0365beb7e2955899fd1d30f`, v2.2.2,
  `agents/*.md`, 68 files) under the LAB method (tiktoken
  `cl100k_base`, per-file frontmatter descriptions, counter verified
  against LAB at its own head: 422 / 469 / 739 exact): description-only
  = **2,728 tokens** (name+desc 3,029; full frontmatter 4,504) — no
  variant reaches ~3.5k. The original derivation is recovered and
  PROVEN as an estimate: roster research summed 14,169 desc chars
  (reproduced exactly from source) and divided by 4 → 3,542; the
  corpus runs ≈5.19 chars/token, so the estimate overstates by ~30%.
  Same construction as the REFUTED ~546. Citable figure: 2,728.
  Evidence: `evals/results/2026-09-30-X2-ecc-rent.md`. Spend: $0.00.

### X3 — Orientation helps Copilot on tasks with headroom (ledger S16)
- Status: UNVERIFIABLE — Copilot base is 3/3 on every task run; no failed
  task exists to test on.
- Cheapest decisive test: mine a harder task band (Copilot base fails ≥2 of
  4 in a screening pass), then 4 tasks × 2 arms, disk-graded.
- Est. cost: $10–18 converted (Copilot burns 3–9× Claude per task).
  Priority: high value, high cost — schedule, don't improvise.

### X4 — ux-ui as an agent (vs skill) pays off
- Status: BLOCKED — agent form waits on a Playwright verification loop;
  Playwright MCP is PARTIAL (works only with `--no-sandbox` in this root
  sandbox).
- Cheapest decisive test: in a non-root environment, one frontend task,
  ux-ui agent with screenshot+assert loop vs base; pass = loop closes
  without human eyes. Est. cost: ~$0.50 + a non-sandbox session.
  Priority: medium.

### X5 — Automatic session-end cleanup/forget in both CLIs
- Status: **Claude trigger PROVEN 2026-09-30** (SessionEnd hook fired 2/2
  headless on Claude Code 2.1.285 + 1/1 via shipped wiring; wired as
  canonical `session_end` → `sidecar.sh record-session-end`, a record
  stub — no cleanup skill exists yet). Copilot side still UNPROVEN.
  Ledger S19; evidence: evals/results/2026-09-30-X5-sessionend-probe.md.
  (Was: UNPROVEN both tools. Claude has documented SessionEnd /
  PostToolUseFailure hooks; Copilot `sessionEnd` output is not processed
  and the installed CLI's failure-hook surface is REFUTED (ledger S4).)
- Cheapest decisive test (Claude): register a SessionEnd hook that writes
  a marker + performs one cleanup action; run a headless session to
  completion; check marker and effect on disk. Copilot: probe whether
  sessionEnd fires at all under trust. Est. cost: ~$0.20. Priority: high
  — the talk close describes this loop as design intent; keep it labeled
  intent until this lands.

### X6 — Hash-pin + audit-check enforcement on skill import
- Status: **PROTOTYPE BUILT + demo-verified 2026-09-30**
  (`scripts/import_skill.py`: audit → import → SHA-256 pin in
  `canonical/skill-pins.json`, `verify` re-hashes; tampered skill
  REFUSED with 4 critical findings, clean skill pinned, post-import
  edit caught). Pattern-list scope only; not wired into install.sh,
  no signatures. Ledger S19; evidence:
  evals/results/2026-09-30-X6-hashpin-prototype.md.
  (Was: UNBUILT (packet finding 5: nobody enforces snapshot + hash-pin +
  audit-check; Snyk ToxicSkills: 36.8% ≥1 flaw, 13.4% critical, 76
  confirmed malicious of 3,984).)
- Cheapest decisive test: prototype import path — snapshot skill, sha256
  pin, refuse on hash mismatch or critical audit verdict; demo against one
  tampered skill and one clean skill. Est. cost: $0 API, build time only.
  Priority: high — the only forward-looking claim in the packet.

### X7 — planner / code-explorer provisional roster entries earn their place
- Status: UNVERIFIABLE — no kill test defined or run for either.
- Cheapest decisive test: S11-protocol A/B, one provisional agent, 4 mined
  tasks, discordant-pair rule; kill = no discordant win and cost ≥ base.
  Est. cost: ~$1–2 per agent. Priority: medium.

### X8 — Wiki orientation improves success vs no-wiki baseline (ledger S3)
- Status: UNVERIFIABLE — eval E3 written, never run. S12 covers a related
  claim on real code; E3's seeded-wiki design is distinct.
- Cheapest decisive test: run E3 exactly as specified in
  `evals/tasks/E3-wiki-value.md`. Est. cost: ~$1–3. Priority: medium.

### X9 — Cross-tool agent parity on the same task (ledger S6)
- Status: UNVERIFIABLE as designed — components landed instead: S6a
  PROVEN (Claude backend, rerun), S6b REFUTED (Copilot pilot: claimed 22
  passed, disk +0 −0).
- Cheapest decisive test: re-run the E6 protocol with disk grading on
  both tools, same task package. Est. cost: ~$1. Priority: medium.

### X10 — Specialist agent pays at higher n / harder tasks (ledger S11)
- Status: UNVERIFIABLE — n=4, zero discordant pairs, descriptively
  cost-negative (+55% turns, +8.5% cost).
- Cheapest decisive test: extend to 8 tasks in a harder band, same
  protocol. Est. cost: ~$3–5. Priority: medium — a REFUTED here would
  retire the roster's agent thesis; a PROVEN would reverse the packet's
  finding 1, so the test must be pre-registered either way.

### X11 — Copilot failure-capture hook (ledger S4, Copilot arm)
- Status: REFUTED on installed CLI v1.0.89 (binary contains no hook
  loader; 0/5). Non-shell tool classes untested (E4).
- Cheapest decisive test: on the next Copilot CLI release, re-run the E4
  Copilot arm unchanged. Est. cost: ~$0.30. Priority: low — version-watch.

### X12 — Note-exclusion rule generalizes (ledger S5)
- Status: PARTIAL — token axis PROVEN (38% cut); quality narrowed-claim
  PROVEN on a synthetic corpus; broad claim REFUTED as scored.
- Cheapest decisive test: re-run E5 against the real wiki (this repo's
  `wiki/`) instead of the seeded corpus. Est. cost: ~$0.50.
  Priority: medium.

### X13 — Copilot `--agent` path for the other 11 agents (ledger S15)
- Status: UNVERIFIABLE — proven for code-reviewer only (201 s, cold-cache
  MCP startup fragile); delegation is the proven path for all 12.
- Cheapest decisive test: marker-invoke 3 more agents via `--agent` with
  a warm MCP cache. Est. cost: ~$1 + ~10 min wall. Priority: low.
- **Result 2026-10-01: REFUTED for planner, security-reviewer, backend**
  under the warm-cache arm with the emitted `.github/mcp.json` in place
  — 3/3 killed at 300 s, zero model calls. Mechanism: `--agent`
  serializes MCP startup (60 s lifecycle failure per server, second
  pass), plain-session control in the same tree completed in 186 s
  with parallel startup. Warm cache is not the binding constraint.
  Remaining 8 agents on this path: still UNVERIFIABLE individually,
  but the path-level mechanism is agent-independent. Cheapest
  follow-up: one agent with `.github/mcp.json` removed (X17 config).
  Evidence: `evals/results/2026-10-01-X13-agent-warmcache.md`.

### X14 — GitHub MCP authenticated operations (ledger S14 carve-out)
- Status: UNVERIFIABLE — token ships empty by design; public search works
  unauthenticated.
- Cheapest decisive test: set a real token, run one authenticated op.
  Requires Samuel's credential action. Est. cost: $0. Priority: blocked
  on human; park.

### X15 — run-eval.sh default path (auto-clone + venv bootstrap) (ledger S17)
- Status: **PROVEN 2026-09-30 (this run)** — see Landed above; ledger S17
  amended, carve-out closed.
- Cost as run: $0.1145 + ~6.7 min wall including one-time clone/venv.

### X16 — Install-surface leftovers (install matrix)
- Status: UNVERIFIABLE ×2 — Claude remote (GitHub) marketplace add/install
  not tested (local PROVEN); `npx skills --copy` mode not tested.
- Cheapest decisive test: one probe each, matrix protocol.
  Est. cost: ~$0.30 each. Priority: low.

### X17 — Copilot custom agents receive repo orientation
- Status: **PROVEN** 2026-09-30 (X17 probe) — as-emitted custom agents
  DO receive AGENTS.md on CLI 1.0.89 (`--agent` path); the v1.0.86
  opt-in statement does not hold behaviorally on this surface and the
  flag is a no-op. Ledger S18;
  `evals/results/2026-09-30-X17-copilot-agent-orientation.md`.
  Original framing (superseded): since CLI v1.0.86 repo
  instruction files are opt-in per agent (`include-custom-instructions:
  true`), and our emitted `.github/agents/*.md` do not set it.
- Cheapest decisive test: body-only-fact probe (packet's own probe lesson:
  description-derived answers pass falsely) — ask an emitted Copilot
  custom agent for a fact that exists only in `AGENTS.md` body text.
  Est. cost: ~$0.50–1.00 (Copilot burn). Priority: high — a REFUTED here
  is a hole in the "one setup, both tools" story.

### X18 — Canonical instruction debt (prompt-audit fix queue)
- Status: OPEN FIXES, not an experiment — 12 suspect patterns (10 in two
  ECC-derived TDD files) and 4 broken references: `researcher` agent (×5)
  and `architect` invoked but nonexistent (canonical: `code-architect`);
  `security-review` skill nonexistent; `tdd-workflow` Step 0 mandates
  `scripts/setup-package-manager.js`, which does not exist.
- Cheapest decisive action: fix or remove each reference; re-run the
  audit scan; zero broken references is the bar. Est. cost: $0.
  Priority: high — post-demo joint review list (addendum).

### X19 — CLAUDE.md deletion + version-aware guard probe
- Status: BLOCKED on Samuel's ruling (keep the `@AGENTS.md` bridge vs
  delete + guard). Facts are settled: native AGENTS.md load needs Claude
  ≥ v2.1.277; annex-only CLAUDE.md suppresses the shared file (2/2).
- Cheapest decisive test (buildable regardless of ruling): guard probe
  that fails if Claude < v2.1.277, if a CLAUDE.md appears without the
  bridge, or if the AGENTS.md marker stops loading. Est. cost: ~$0.20.
  Priority: high once ruled.

### X20 — Roster narrative drift (packet vs wiki vs canonical/)
- Status: OPEN inconsistency found this run. `wiki/notes/v2-roster.md`
  records the earlier W2 derivation (planner, code-reviewer,
  security-reviewer, tdd-guide, build-error-resolver, code-explorer +
  backend) and still says live-tool discovery is UNVERIFIED — overtaken
  by S14 PROVEN. The packet's roster v2 (explorer, code-reviewer,
  task-runner, build-error-resolver, security-reviewer, evaluator +
  provisional planner, code-explorer) exists only in the packet: no
  canonical files for `task-runner` or `evaluator`, and "explorer" /
  provisional "code-explorer" appear to name the same file twice.
- Cheapest decisive action: one roster decision recorded in one place;
  create or retire the two missing agent files; correct the note.
  Est. cost: $0. Priority: high — three sources currently tell three
  roster stories.

- Resolution — 2026-09-30 (X20 run, branch `fix/roster-drift`):
  CLOSED. One roster decision recorded in one place:
  `wiki/notes/v2-roster.md`, correction of 2026-09-30 (X20 run).
  Roster of record = the 12 files in `canonical/agents/` (all
  installed by `install.sh`, no tier filter in `install_agents()`;
  invocation status ledger S14 PARTIAL, not PROVEN — the W2 note's
  UNVERIFIED line and the triage "S14 PROVEN" citation are both
  corrected there). `task-runner` and `evaluator`: no canonical
  file at head or in any commit tree — recorded not-built/retired,
  no files created. `explorer`: REFUTED as a separate agent; the
  only matching file is `code-explorer.md`, counted once. Packet
  roster v2 retired as a shipped-state description (dated
  correction appended to the packet). Spend: $0.

### X21 — Opus 5.5 degrades older prompts (ledger C3)
- Status: UNVERIFIABLE as a general claim; narrow patterns partially
  supported (prefill removal, effort default). Anthropic's own guides say
  prior-generation prompts should generally carry over.
- Cheapest decisive test: paired prompt A/B across model generations on
  a fixed task set with planted legacy scaffolding. Est. cost: ~$2–4.
  Priority: low — external claim, not load-bearing for the setup.

## Next 3 by value/cost

1. **X15** — run-eval default path: ~$0.10, closes the last carve-out on
   the feedback-loop claim the talk leans on. (In flight.)
2. **X17** — Copilot custom-agent orientation probe: ~$0.50–1.00, tests a
   documented trap sitting inside the core "one setup, both tools" claim.
3. **X5** — Claude SessionEnd cleanup probe: ~$0.20, converts the talk
   close's design intent into a verdict one way or the other.
