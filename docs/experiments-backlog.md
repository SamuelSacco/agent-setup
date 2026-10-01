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
- **Resolution 2026-10-01 (X1 run, branch `lab/x1-toolset-ab`):
  outcome question tested at partial n — standing verdict
  UNVERIFIABLE as a stable effect.** Arms: full default (14 defs
  loaded) vs restricted `--tools` set of 6 (Read, Write, Edit, Bash,
  Grep, Glob), Haiku 4.5, packaged tasks. Completed pairs: 1 of 4
  (nx-t2 discordant: full FAIL $0.299612/13t, restricted PASS
  $0.055467/7t — the pre-registered rule fired PROVEN at n=1).
  nx-t3: restricted FAIL ($0.286612/11t), full arm lost to an
  execution-layer incident (backgrounded launches executed twice;
  duplicate billing, partly unmetered; series stopped under the
  $1.50 cap, rich pairs never launched). The nx-t2 discordance does
  not stand as an effect: a duplicate execution of the identical
  full arm on nx-t2 PASSed with a correct fix (tree verified), so
  the pair's outcome is execution-dependent. Side-finding PROVEN by
  raw-body capture: `--tools` restricts loaded defs to exactly the
  named set (6/6); `--allowedTools` alone does not (14 loaded).
  Metered spend $0.672354 of $1.50 cap (+ unmetered duplicate
  spend, est. total billed $0.87–1.17). Evidence:
  `evals/results/2026-10-01-X1-toolset-ab.md`. A clean rerun at
  full n=4 needs a non-duplicating execution path and ~$1.50
  metered headroom at 2026-10-01 prices.

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
- **Update 2026-10-01 (screening wave, branch `lab/x3-screening`):**
  band NOT constructed; status remains UNVERIFIABLE. Mining succeeded:
  9 candidates with disk-verified discriminating oracles committed
  under `evals/tasks-packaged/` (nx-t5..t8, rich-u5..u7, click-c1/c2).
  Screening produced zero valid grades — click-c1's only run graded
  invalid (src-layout grading-env defect; remedy `PYTHONPATH=src`
  validated at $0), the rich worker's all-PASS report was void (no
  artifacts on disk), nx never launched. Verified spend $2.82; the
  rich worker claimed a further $10.24, unverifiable. Side findings:
  `run_eval.py` Copilot cost parse broken under CLI 1.0.90 lowercase
  footer suffixes (fixed on the branch); every runner-written Copilot
  cost field under 1.0.90 under-reports. Evidence:
  `evals/results/2026-10-01-X3-screening-results.md`. Next: fresh cap
  decision, then re-screen click (PYTHONPATH=src) → nx → rich, then
  the pre-registered A/B.
- **Correction 2026-10-01 ~05:15 UTC:** the sentence above voiding
  the rich worker's report is retracted (see the results doc's
  Correction section — the coordinator checked disk mid-flight).
  rich-u5 was validly screened: Copilot base PASS 2/2, screened out.
  Verified wave spend is $6.99 of the $8 cap (no breach). Still
  unscreened: rich-u6/u7, click-c2, nx-t5..t8; click-c1's grade
  still invalid (§6 of the results doc). Band still not
  constructed; X3 still UNVERIFIABLE.
- **Update 2026-10-01 (Wave 4-A re-screening, branch
  `lab/x3-screening`):** fresh caps ($25 screening; A/B $18
  contingent on band ≥ 4). Stage 1 completed for 4 of the 7
  remaining candidates, all footer-verified on disk: click-c1
  PASS 2/2 (screened out; `PYTHONPATH=src` remedy confirmed in
  production — grades are real this time), nx-t5 PASS 2/2,
  nx-t6 PASS 2/2, and **click-c2 FAIL 2/2 — the first Copilot base
  failure signal of the X3 effort; click-c2 is IN the band**.
  Verified spend $24.9025 of the $25 cap; the cap bound before
  nx-t7, nx-t8, rich-u6, rich-u7 (still unscreened). Band = 1
  member < 4, so the pre-registered A/B did not run; X3 remains
  UNVERIFIABLE. Calibration: click-c2 cost $4.45/run (↑4.3M
  input) — the $2.20/run planning figure understates click-class
  runs ~2×; finishing stage 1 needs roughly another $25 cap.
  Evidence: `evals/results/2026-10-01-X3-wave4a-rescreen-results.md`.

### X4 — ux-ui as an agent (vs skill) pays off
- Status: **REFUTED 2026-10-01** (branch `lab/x4-ux-ui-loop`,
  prereg `d76f61e`) — the Playwright loop ran in this root sandbox
  (scratch config: canonical args + `--no-sandbox`, system
  Chromium via `--executable-path`, `file://` navigation; loopback
  HTTP is blocked by Chromium LNA checks here). One planted-defect
  frontend task, Haiku 4.5, independent Playwright assertion
  oracle: base CLOSED the loop (navigate → screenshot → 3 edits →
  re-navigate → clicks → evaluate; assertion PASS; 18 turns,
  $0.0964). The ux-ui agent did NOT close it — zero Playwright
  calls: its emitted `tools: [Read, Write, Edit, Bash]` allowlist
  (from canonical `tools_hint`, ledger S21) excludes every
  `mcp__playwright__*` tool, so the browser loop its own working
  rules require is unreachable as installed. It fixed all 3
  defects from source and self-verified via curl + a Node DOM
  simulation (final tree passes the assertion; 12 turns, $0.0425)
  — correct fixes, no browser loop. Ledger S29; evidence:
  evals/results/2026-10-01-X4-ux-ui-loop.md. A retest needs an
  MCP-capable ux-ui allowlist — a canonical change, not a rerun.
  (Was: BLOCKED — agent form waits on a Playwright verification
  loop; Playwright MCP is PARTIAL (works only with `--no-sandbox`
  in this root sandbox).)
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
  **Update 2026-10-01: Copilot trigger PROVEN** — `sessionEnd` fired
  3/3 headless on Copilot CLI 1.0.89 (repo `.github/hooks/*.json`,
  trust via `COPILOT_ALLOW_ALL=true`; `sessionStart` control 3/3;
  terminations were complete/abort/error — provider unreachable for
  2 trials, no clean successful-turn exit isolated). X5 trigger
  question closed for both tools; remaining work is the cleanup
  procedure itself, not the trigger. Evidence:
  evals/results/2026-10-01-X5-copilot-sessionend.md.
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
- Status: UNVERIFIABLE — both halves kill-tested 2026-10-01; neither kill rule met, no discordant win in either half.
  [PLANNER HALF TESTED 2026-10-01 (branch wave2c/x7-planner-kill-test):
  still UNVERIFIABLE — 4 paired planning tasks on committed fixtures,
  all 8 runs 5/5 on content checks, zero discordant pairs, agent
  cheaper ($0.202 vs $0.320) so the kill rule is not met and no
  discordant win earns the place. The prereg's fabrication clause,
  transplanted from the tracing protocol, misclassifies proposed
  new files; a decisive rerun needs that clause scoped to paths
  cited as existing, plus harder/larger codebases. Code-explorer
  half unchanged here (separate worker). Evidence:
  evals/results/2026-10-01-X7-planner-prereg.md;
  evals/results/2026-10-01-X7-planner-results.md. Spend $0.522.]
  [CODE-EXPLORER HALF TESTED 2026-10-01 (branch wave2c/x7-code-explorer-kill-test): code-explorer: kill test RUN 2026-10-01 (ledger S28), verdict   UNVERIFIABLE — 4 paired NetworkX exploration tasks, base 4/4 vs   agent 4/4, zero discordant pairs; kill rule not met (agent cost   $0.1526 < base $0.1970, −22.5%); PROVEN bar (discordant win) also   not met. Base had no headroom at this difficulty; a decisive   re-test needs harder tasks the base arm fails. Evidence: evals/results/2026-10-01-X7-code-explorer-results.md. Spend $0.3496.]
- Cheapest decisive test: S11-protocol A/B, one provisional agent, 4 mined
  tasks, discordant-pair rule; kill = no discordant win and cost ≥ base.
  Est. cost: ~$1–2 per agent. Priority: medium.

### X8 — Wiki orientation improves success vs no-wiki baseline (ledger S3)
- Status: UNVERIFIABLE — eval E3 written, never run. S12 covers a related
  claim on real code; E3's seeded-wiki design is distinct.
- Cheapest decisive test: run E3 exactly as specified in
  `evals/tasks/E3-wiki-value.md`. Est. cost: ~$1–3. Priority: medium.
- **[RESOLVED 2026-10-01 (X8 run): PROVEN** — A 5/5 vs B 1/5 across
  5 task types (bugfix, extend-feature, answer-from-history,
  refactor-per-convention, find-the-decision), token overhead −41%
  (A cheaper; the B arm burned tokens hunting for absent info).
  Seeded "ledgerlite" fixture; facts existed only in wiki notes.
  T4 both passed — convention recoverable from in-tree code, so
  T4 diluted the contrast. 4 escape attempts handled under a
  read+reflected contamination rule (2 discarded); the counted B
  answer-task artifacts stayed genuine baseline failures. Total
  spend ≈ $1.16 of $3.00 cap. Evidence:
  `evals/results/2026-10-01-X8-e3-wiki-value.md`.]

### X9 — Cross-tool agent parity on the same task (ledger S6)
- Status: DONE 2026-10-01 — decisive test run as specified (both
  prereg arms, disk grading, same task package): S6 PROVEN at the
  threshold boundary (blind 10 vs 9, diff 1 ≤ 1; probe 4/4 and
  grader pytest pass on both arms), $0.754 of $2 cap. UNVERIFIABLE
  as designed stands only for the full 3×3 grid, which was never
  specified. See `evals/results/2026-10-01-X9-e6-parity.md`.

### X10 — Specialist agent pays at higher n / harder tasks (ledger S11)
- Status: DONE 2026-10-01 — REFUTED (ledger S11 amended). Pre-registered
  8-task harder band; 5 pairs completed before Anthropic API credit
  exhaustion truncated H8/H9/H10 (spend $3.98 of $5 cap): base 3/5,
  specialist 1/5, net discordant −2, firing the pre-registered REFUTED
  line. Remaining decisive test if the verdict is ever revisited:
  re-run the 3 unrun pairs (H8/H9/H10) unchanged from the prereg once
  credit is restored. Est. cost: ~$1.5–2.5.
- Original note: UNVERIFIABLE — n=4, zero discordant pairs, descriptively
  cost-negative (+55% turns, +8.5% cost). Cheapest decisive test was:
  extend to 8 tasks in a harder band, same protocol, pre-registered
  either way.

### X11 — Copilot failure-capture hook (ledger S4, Copilot arm)
- Status: REFUTED on installed CLI v1.0.89 (binary contains no hook
  loader; 0/5). Non-shell tool classes untested (E4).
- Cheapest decisive test: on the next Copilot CLI release, re-run the E4
  Copilot arm unchanged. Est. cost: ~$0.30. Priority: low — version-watch.
- **Version-watch 2026-10-01 (branch `lab/x11-version-watch`):**
  installed CLI is 1.0.90, a real newer release (npm tree = 1.0.89
  launcher; running build auto-updates into
  `~/.cache/copilot/pkg/linux-x64/1.0.90/`; transition between the
  04:13:09Z and 04:19:55Z sessions tonight). E4 Copilot arm re-run
  unchanged on 1.0.90: **0/5, REFUTED stands** — exits 127/1/1/1/2,
  hook loader active under trust, sidecar never invoked; mechanism
  unchanged (shell `tool.execution_complete` reports `success: true`,
  failure only in result text). Spend $0.0984 converted of $0.75.
  Evidence: `evals/results/2026-10-01-X11-version-watch.md`.
  Next watch: re-run on the first release after 1.0.90.

### X12 — Note-exclusion rule generalizes (ledger S5)
- Status: PARTIAL — token axis PROVEN (38% cut); quality narrowed-claim
  PROVEN on a synthetic corpus; broad claim REFUTED as scored.
- Cheapest decisive test: re-run E5 against the real wiki (this repo's
  `wiki/`) instead of the seeded corpus. Est. cost: ~$0.50.
  Priority: medium.
- **Resolution 2026-10-01 (branch lab/x12-e5-real-wiki):** re-run done;
  PARTIAL narrows, generalization fails. Real wiki at ce0edbe = 16
  notes, all active (0 archived/stale), so token cut = 0.0%
  (REFUTED vs ≥30% bar; the 38% was the seed's 37.5% archived share).
  Quality 10/10 in both settings, 0 inventions — vacuous, settings
  byte-identical; differential quality effect UNVERIFIABLE until the
  real wiki holds archived/stale notes. Spend $0.0672358 of $0.50.
  Evidence: `evals/results/2026-10-01-X12-e5-real-wiki.md`.

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
- **Q15 isolation 2026-10-01: REFUTED** — the serialized-startup mechanism
  is not triggered by the emitted `.github/mcp.json` alone: `planner`,
  same X13 task, scratch HOME (no user-scope MCP config), CLI 1.0.90,
  warm cache — with-file 41 s exit 0 (all 5 workspace servers connected),
  without-file 22 s exit 0. X13's 3× 300 s stalls (real HOME, CLI 1.0.89,
  user-scope duplication) do not reproduce; the 60 s lifecycle failures
  themselves did not occur, so their trigger is unlocated. The stall is
  environment-bound, not file-bound. Evidence:
  `evals/results/2026-10-01-X13-mcp-isolation.md`.

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
- Status: **PROVEN ×2 2026-10-01 (Wave 4-B)** — Claude remote (GitHub)
  marketplace add/install PROVEN (anonymous HTTPS clone, payload in
  shared cache keyed by git SHA, `plugin list` scope user/enabled);
  `npx skills --copy` PROVEN (real copied dirs in canonical store +
  `~/.claude/skills`, zero symlinks, `diff -r` vs source empty; Copilot
  served via the canonical store, no `~/.copilot/skills` created).
  Ledger S27; `evals/results/2026-10-01-X16-install-surface.md`.
  Cost as run: $0.00.

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
- Status: CLOSED 2026-10-01 (X18 run, branch `fix/x18-instruction-debt`) —
  see resolution note below.
- (Original status: OPEN FIXES, not an experiment — 12 suspect patterns (10 in two
  ECC-derived TDD files) and 4 broken references: `researcher` agent (×5)
  and `architect` invoked but nonexistent (canonical: `code-architect`);
  `security-review` skill nonexistent; `tdd-workflow` Step 0 mandates
  `scripts/setup-package-manager.js`, which does not exist.
- Cheapest decisive action: fix or remove each reference; re-run the
  audit scan; zero broken references is the bar. Est. cost: $0.
  Priority: high — post-demo joint review list (addendum).

- Resolution — 2026-10-01 (X18 run, branch `fix/x18-instruction-debt`):
  CLOSED. Re-verified all 16 audit items on disk at master `ce0edbe`:
  the 2026-09-30 fix (`297285e`, merged `82ea351`) had landed 11 of 12
  suspect patterns and all 4 broken references (`researcher` ×5 →
  subagent/research pass; `architect` → `code-architect`;
  `security-review` → `verification-loop`; `setup-package-manager.js`
  mandate → lockfile/`packageManager` detection), but never closed
  this item and missed one pattern. Residual fixed here: planner's
  77-line Stripe worked example (audit stale-example #12) removed,
  replaced with a 16-line outline; adapters regenerated via
  `scripts/install.sh`. Final scan over 61 shipped-surface files
  (canonical + `.claude/` + `.github/` + root `AGENTS.md`): broken
  references 0, suspect markers 0, exit 0 — before this run:
  broken 0, suspect 1 pattern (3 surface hits). No claims-ledger
  entry references X18; no ledger change. Evidence:
  `evals/results/2026-10-01-X18-instruction-debt.md`. Spend: $0.

### X19 — CLAUDE.md deletion + version-aware guard probe
- Status: BLOCKED on Samuel's ruling (keep the `@AGENTS.md` bridge vs
  delete + guard). Facts are settled: native AGENTS.md load needs Claude
  ≥ v2.1.277; annex-only CLAUDE.md suppresses the shared file (2/2).
- Cheapest decisive test (buildable regardless of ruling): guard probe
  that fails if Claude < v2.1.277, if a CLAUDE.md appears without the
  bridge, or if the AGENTS.md marker stops loading. Est. cost: ~$0.20.
  Priority: high once ruled.
- Resolution — 2026-10-01 (X19 run, branch `feat/x19-version-guard`):
  GUARD BUILT. `scripts/check-version-guard.sh` (standalone; the C4
  guard `scripts/check-agents-md-load.sh` is untouched — it waives the
  floor when a bridged CLAUDE.md is present and checks only the root
  file). The X19 guard fails (exit 1) on: (1) Claude < 2.1.277,
  unconditional (shim-induced 2.1.276 → exit 1; exactly 2.1.277 →
  pass; `v`-prefixed / bare / prefixed version strings all parse);
  (2) any CLAUDE.md in the tree without the `@AGENTS.md` bridge
  (root and nested-only both caught; bridged control passes);
  (3) marker missing from AGENTS.md (static) or not loading live
  (marker-removed tree → probe `NOT LOADED`, exit 1; clean tree live
  probe → marker loaded, exit 0). All three conditions PROVEN.
  Evidence: `evals/results/2026-10-01-X19-version-guard.md`.
  Spend: $0.0459424 metered (≈$0.061 incl. one unreported probe run).
  The keep-vs-delete CLAUDE.md ruling itself remains PARKED for
  Samuel — nothing was deleted and no bridge was changed (at head
  the tree already ships no CLAUDE.md, per the C4 final shape).

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
- Status: DONE 2026-10-01 (branch lab/x21-prompt-ab) — C3 REFUTED on the
  test: legacy 4/5 on claude-opus-5-5 and on claude-opus-5, modern 4/5 vs
  5/5. Preregistered decision rule applied. Spend ~$0.10 of $3.50 cap.
- Cheapest decisive test: paired prompt A/B across model generations on
  a fixed task set with planted legacy scaffolding. Est. cost: ~$2–4.
  Priority: low — external claim, not load-bearing for the setup.
  Evidence: evals/results/2026-10-01-X21-prompt-ab.md

## Next 3 by value/cost

1. **X15** — run-eval default path: ~$0.10, closes the last carve-out on
   the feedback-loop claim the talk leans on. (In flight.)
2. **X17** — Copilot custom-agent orientation probe: ~$0.50–1.00, tests a
   documented trap sitting inside the core "one setup, both tools" claim.
3. **X5** — Claude SessionEnd cleanup probe: ~$0.20, converts the talk
   close's design intent into a verdict one way or the other.
