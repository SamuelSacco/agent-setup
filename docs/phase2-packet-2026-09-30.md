# Phase 2 packet — 2026-09-30 (raw material for the 14:00 build)

Everything below is measured. Verdicts: PROVEN / REFUTED / UNVERIFIABLE /
PARTIAL. Sources in `evals/results/2026-09-30-P2-*` and
`hidden_files/research/2026-09-30-P2-*` on this branch. V1 is untouched
(tag `v1`, master at 2021d60).

## The five findings that matter

1. **Specialist agents do not pay on real code; orientation does.**
   NetworkX (~121k LOC), tasks mined from real fix commits, oracle-validated,
   disk-graded. Claude arms, 4 tasks each: base 3/4 · 73 turns · $1.164;
   +backend agent 3/4 · 113 turns · $1.263; +orientation 4/4 · 77 turns ·
   $0.967. Agent claim UNVERIFIABLE (no discordant pair; +55% turns, +8.5%
   cost, zero added solves). Orientation REPLICATED same day on 4 new tasks:
   base 3/4, orientation 4/4. Combined n=8: orientation 8/8 vs base 6/8
   (success effect consistent; cost effect mixed — replication had
   orientation at $0.898 vs base $0.662).
2. **Self-report is not evidence — caught live, again.** Base Claude on the
   hardest task left its checkout, applied its fix to the evaluator's sibling
   clone, ran tests there, reported "All 106 existing tests pass." Its own tree: zero
   changes. Same family as the V1 Copilot E6 fabrication (claimed 22 passed,
   disk +0 −0). Disk grading caught both.
3. **`npx skills add` covers both tools; nothing else does.** Skills CLI
   (Vercel Labs) installs to a canonical `.agents/skills/` store; Copilot
   reads it natively, Claude gets a symlink in `.claude/skills/`. Trap:
   a Claude-only project install silently copies into `.claude/skills/`
   with no canonical copy (drift). Agents/hooks/MCP/plugins via npx: not
   paths. In-tool and canonical paths fill the rest — full matrix in
   `evals/results/2026-09-30-P2-install-matrix.md`.
4. **CLAUDE.md stays.** Native AGENTS.md load on Claude 2.1.285 PROVEN
   (2/2) — and the suppression trap PROVEN (2/2): an annex-only CLAUDE.md
   silently stops the shared file loading. Dropping the `@AGENTS.md` bridge
   buys a silent failure mode. Verdict PARTIAL. Qualifiers (docs-checked
   2026-09-30): suppression is the DEFAULT memory mode's behavior;
   native AGENTS.md load requires Claude Code ≥ v2.1.277; user-level and
   managed CLAUDE.md do not trigger suppression. Under Samuel review:
   delete + version-aware guard probe (see 14:00 agenda).
   **Correction 2026-09-30 (W3, Samuel's 14:24 directive): finding
   superseded — CLAUDE.md is DELETED on branch `change/no-claudemd`,
   replaced by guard `scripts/check-agents-md-load.sh` (fails on
   version < 2.1.277 with no CLAUDE.md, on any bridgeless CLAUDE.md,
   or on a failed live marker probe; wired as run-eval's preflight).
   Final shape re-proven live: Claude 2.1.285 marker load 2/2,
   Copilot 1.0.89 1/1; negative controls exit 1. Ledger C4 amended;
   evidence: `evals/results/2026-09-30-P2-claudemd-final-shape.md`.**
5. **The ecosystem's gap is enforcement.** Skills supply chain (Snyk
   ToxicSkills, 3,984 skills): 36.8% ≥1 flaw, 13.4% critical, 76 confirmed
   malicious. Audit verdicts ship in install metadata, coverage spotty,
   nothing blocks. A top skill (683K installs) fetches instructions from a
   remote URL at runtime. Nobody enforces snapshot + hash-pin + audit-check
   on import. Candidate V2 differentiator.

## Setup state after Phase 2 (all live-invoked, both tools)

- 12 agents PROVEN (marker tasks, both tools). 8 skills PROVEN (Skill/skill
  tool events, both tools). 5 MCP servers: context7, sequential-thinking,
  filesystem-wiki, github PROVEN both tools; playwright PARTIAL (sandbox
  Chrome/root limits only; works with `--no-sandbox`).
- Copilot `--agent` path PROVEN for code-reviewer (201 s for a trivial
  task — slow; cold-cache MCP startup is fragile). Delegation is the
  reliable path for all 12.
- Bug found and fixed: `.github/mcp.json` shipped the wrong key (`servers`);
  Copilot rejected it. V1's Copilot MCP worked only via the root `.mcp.json`
  accident. Both keys now emitted; Copilot lists all 5 workspace servers.
- ECC: 668 items inventoried → 19 ported to `canonical/` (MIT, attribution
  headers), 223 port-with-changes, 426 skipped with reasons.
- Roster v2: 6 default + 2 provisional, ~300 tokens of description rent
  (vs ~546 for the V1 12, ~3.5k for all-68 ECC). Default: explorer,
  code-reviewer, task-runner, build-error-resolver, security-reviewer,
  evaluator (data-scientist reborn, no edit rights). backend → skill,
  ux-ui → skill (agent form blocked on a Playwright verify loop),
  data-scientist/ux-ui agents demoted to optional. Inherited three proven
  to share identical model/tool hints — one agent, three hats.
  - **Correction 2026-09-30 (W2 triage lab):** the rent figures above do
    not reproduce from the files. Re-measured (tiktoken cl100k on
    `canonical/agents/*.md` frontmatter): all 12 = 422 tokens
    description-only (469 with names), not ~546; the roster-v2 six map
    to only five files (178 tokens) — `task-runner` has no canonical
    file — and total at most 227, not ~300. The ~3.5k ECC figure is
    unverifiable from this repo. Direction (six ≈ half of twelve)
    survives; the numbers do not. Also: no per-agent tool restriction
    is emitted by the adapters (hints are stripped, zero `tools:`
    allowlists) — every agent loads the full session toolset (Claude
    default 12 defs, Copilot default 23). Evidence:
    `evals/results/2026-09-30-LAB-rent-toolcounts.md`; backlog X1/X2/X20
    in `docs/experiments-backlog.md`.
  - **Correction 2026-09-30 (X2 remainder):** the ~3.5k ECC figure is
    now resolved — REFUTED as a token figure, retired. Re-derived from
    the ECC source at the mined commit (`affaan-m/ECC` `c70874f`,
    v2.2.2, `agents/*.md`) under the LAB tiktoken cl100k method:
    all-68 description rent = **2,728 tokens** (3,029 with names), not
    ~3.5k. The original number is a chars÷4 estimate: 14,169 desc
    chars (reproduced exactly from source) / 4 = 3,542; the corpus
    runs ≈5.19 chars/token. Citable figure: 2,728. Evidence:
    `evals/results/2026-09-30-X2-ecc-rent.md`; backlog X2 closed.
- Copilot surfaces: plugins exist fully (`copilot plugin install`,
  marketplace repos; Anthropic's plugin repo is addable per GitHub docs);
  skills strongest crossover (`.github/`, `.agents/`, `.claude/` all read);
  two behavioral divergences only — directory-trust gating and
  `postToolUseFailure` not firing for shell-exit failures (live-tested;
  the event is documented generically — the shell gap is empirical only,
  do not state it as a universal). Also: Copilot custom agents do NOT
  inherit repo instruction files automatically — since CLI v1.0.86 they
  opt in per agent definition (`include-custom-instructions: true`).
- Say carefully: session-harden skill invocation PROVEN both tools;
  automatic session-close triggering is NOT fully proven on Copilot
  (sessionEnd event documented, trust-gated). Do not upgrade this claim
  on stage.

## Adoption ("drop this in")

- quickstart.sh prototype: one command, 0 decisions, 2 unavoidable human
  actions (vendor auth), exit-2 gate with remedy + idempotent resume.
  Fresh-sim: 30 s warm; 1m58 s cold incl. both npm CLI installs.
- V1 friction found by timing a stranger: README omits the clone command;
  no CLI install commands anywhere (npm measured: Claude 19 s, Copilot
  41 s); prereqs (python3, node) unstated; docs disagree on step order;
  install.sh dirties the tree (32 paths); github MCP ships an empty token
  that fails first launch; repo is PRIVATE (hard gate for any stranger).
- Verification-probe lesson: ask-the-skill's-description probes pass
  falsely (Claude answered from the description). Body-only-fact probes
  pass honestly on both tools at $0.004–0.012 per run.

## Context rent (measured, same probe)

Claude `--bare` 1,866 input tokens · Copilot default 14,510 (~5.9–6.2k
system + ~7.7–8k tool defs, 23 tools) · Claude default 20,589. Never
compare bare Claude to default Copilot — that framing is REFUTED.

## Spend

Phase 2 total ≈ $10.5 of the $15 cap (W3 $5.35; matrix $0.65; W5 $0.12;
replication $1.56; port probes $2.78; onboarding $0.08). Corrected
2026-09-30 after adversarial re-derivation: the port-probe cost log
sums to $2.7768, not <$1. Key balance after Phase 2: roughly $7.7 of
Samuel's reported $18.23, before the late-morning extension streams.
V1 evals: ~$1.03.

## Open risks for 16:00

- Stage-machine auth UNVERIFIED. All proof ran in Helm's sandbox.
  15-min smoke test inside the 14:00 window: open repo, auth both CLIs,
  one skill invocation. Fallback: `docs/demo-backup/`.
- D3 (email V1 deck+guide to Samuel's Gmail) never decided — moot if the
  14:00 build produces a new deck; decide in the room.
- Orientation n=8 is two batches of 4 on one codebase (NetworkX, Haiku).
  Present as measured-here, not as a law. Q&A exposure: two independent
  null results exist — ETH Zurich/LogicStar (arXiv 2602.11988, revised
  2026-09-29: context files did not generally improve success, inference
  cost +>20%) and Khatri (arXiv 2607.27250: 288 runs, no measurable
  correctness effect). Safe stage wording: "NetworkX, Haiku 4.5, our
  orientation protocol: 8/8 vs 6/8." Know both papers before 16:00.
- Copilot precedence is now documented (checked 2026-09-30): first-loaded
  wins for agents/skills, LAST-loaded wins for MCP servers. The
  no-duplicate-names rule stands; "no reliable precedence" is retired.

## Decisions for the room (recommendation first)

1. Narrative: lead with Phase 2 (measured setup v2 + honest negatives)
   over V1's plumbing proof. The A/B table and the caught fabrication
   are the strongest material we own.
2. CLAUDE.md: present the trap result, not the file debate.
3. Supply-chain numbers: include — it's the one forward-looking claim
   (enforcement gap) and it's sourced.

**Correction — 2026-09-30 ~14:35 ET (merge-readiness audit):** the
quickstart above was described in-repo but existed only in worker
scratch. It has now been reviewed and landed at `scripts/quickstart.sh`;
in-tree `--structural-only` run passes (8/8 skills, 12/12 agents, both
MCP configs parse, zero tree delta beyond the new file). The live-probe
path remains gated on vendor auth as designed.

**Correction — 2026-09-30 ~14:55 ET (X17 probe):** the Copilot-surfaces
bullet above states custom agents do NOT inherit repo instruction
files automatically since CLI v1.0.86 (opt-in via
`include-custom-instructions: true`). Behaviorally REFUTED for CLI
1.0.89 `--agent` sessions: an as-emitted custom agent (no flag)
reproduced a body-only AGENTS.md marker exactly, with zero tool
calls; the marker-removed control failed; the debug log shows
AGENTS.md injected as a `<custom_instruction>` block next to the
agent's own instructions. The flag is a no-op on this surface. Do not
state the opt-in trap on stage as CLI behavior; other surfaces
(IDE/cloud) remain untested. Evidence:
`evals/results/2026-09-30-X17-copilot-agent-orientation.md` (S18).
**Update — 2026-09-30 ~14:55 ET (backlog X5):** the session-close item in
the talk close is now scoped by a probe. In Claude Code 2.1.285, a
`SessionEnd` hook fires automatically at the end of headless sessions
(2/2 probe runs + 1/1 via the shipped wiring; ledger S19). Wired in the
repo as a canonical `session_end` hook whose action records the
session-end event to the sidecar store — that record is a stub, not a
cleanup skill; no cleanup procedure runs yet. Copilot remains
UNVERIFIABLE (no hook loader in the installed CLI, S4). Talk wording
should say "the session-end trigger is proven in Claude; the cleanup
procedure on it is not built," not "cleanup runs automatically."

**Update — 2026-09-30 ~14:55 ET (backlog X6):** finding 5's "nobody
enforces snapshot + hash-pin + audit-check on import" now has an
in-repo counterexample at prototype scale: `scripts/import_skill.py`
(audit → import → SHA-256 pin in `canonical/skill-pins.json`, `verify`
re-hashes). Preregistered demo: clean skill pinned (hash matches an
independent `sha256sum`); a planted tampered skill was REFUSED with 4
critical findings (instruction override, pipe-to-shell, credential
exfiltration); a post-import edit was caught by `verify`. Ledger S20.
Prototype limits stand: pattern-list audit, no signatures, not wired
into `install.sh`.

---

**Correction 2026-09-30 ~15:12 ET (claude-opus critique — S12 narrowed):** the orientation treatment tested in S12/S16 was a hand-written, repo-specific orientation file delivered as `CLAUDE.md` — this repo's own `AGENTS.md` and wiki were never the treatment. PROVEN scope: "a hand-written orientation file improves Claude Code + Haiku 4.5 success on NetworkX (8/8 vs 6/8); Rich: null." Do not say "AGENTS.md/wiki orientation is proven" — the wiki question (S3) is UNVERIFIABLE. The combined rule was registered after the NetworkX result was known. Full critique: `docs/claude-critique-2026-09-30.md`. One of the two NetworkX discordant pairs (R2) turned on exception-message wording ("No nodes in graph" vs the test's `null graph` match) — disclosed in the results file and the S12 ledger row. Also corrected by the same critique: S4's Copilot mechanism (hooks fire in trusted dirs; `postToolUseFailure` misses shell failures), S5's token math (uncached −51%, total context −2%, cost −40%; corpus score 5/10), S14 PROVEN → PARTIAL (playwright), and the P2 research sources are now committed under `hidden_files/research/` so packet numbers trace in-repo.

**Correction 2026-09-30 ~15:20 ET (P3 big-model test, ledger S22):** the orientation effect is model-tier-dependent. Identical protocol on `claude-opus-5-5`: NetworkX 3/4 vs 3/4, Rich 3/4 vs 3/4 — zero discordant pairs, verdict UNVERIFIABLE at that tier. Mechanism: headroom. Opus base solves T1 (the task Haiku base failed) unaided; the tasks that still fail (T4, U3) fail identically in both arms at both tiers. Orientation still charged +9% cost per run at Opus tier and bought nothing. Talk wording: "Orientation bought solves where the model had headroom (Haiku 4.5, NetworkX). At the top tier it bought nothing and still charged rent." Also on T4, both Opus arms stopped with zero code changes after concluding the bug was unreproducible — grading still fails them; a stronger model talking itself out of the task is a failure mode worth naming. Full data: `evals/results/2026-09-30-P3-bigmodel-ab.md`. Spend $3.05 of the $14 cap.

**Update 2026-09-30 ~15:25 ET (S6b fair rerun):** the E6 Copilot story is now two-sided. Pilot (default permissions): writes denied, agent fabricated "22 passed" over zero files — REFUTED, stands. Rerun with writes pre-approved (`COPILOT_ALLOW_ALL=true`, same model/credential): real files on disk, 20/20 tests on independent re-run, self-report matched the disk — PROVEN at n=1. The variable was permission mode, the same arc as Claude's pilot → S6a. If E6 comes up: "blocked agents fabricate; pre-approved agents did the work — disk grading caught the first and confirmed the second." Evidence: `evals/results/2026-09-30-S6B-preapproved-rerun.md`. Spend $0.39 converted.
