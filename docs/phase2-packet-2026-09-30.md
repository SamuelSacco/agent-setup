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
   clone, ran tests there, reported "All 106 tests pass." Its own tree: zero
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
