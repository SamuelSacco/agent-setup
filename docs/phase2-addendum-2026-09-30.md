# Phase 2 addendum — 2026-09-30, late-morning extension streams

Consolidates the seven streams run 11:12–11:45 ET under Samuel's
"don't let me be the bottleneck" directive. Companion to
`docs/phase2-packet-2026-09-30.md`. All verdicts disk-derived.

## Headline, revised

**Orientation: 11/12 vs base 9/12 across two codebases — every deciding
pair is NetworkX's; on the second codebase the effect was zero.**
Second codebase: Textualize/rich @ 9d8f9a37 (~26.6k LOC, terminal
rendering). Same model (Haiku 4.5), same arms, pre-registered
(prereg `d85c6e5` before any run). Rich: base 3/4, orientation 3/4,
zero discordant pairs → UNVERIFIABLE there. The single base failure
(U3, cells/ZWJ width) was failed identically by the orientation arm —
same partial fix, same missed branch. Combined n=12 verdict PROVEN
stands under the pre-registered combined rule (ledger S12, amended).
Stage wording: "NetworkX, Haiku 4.5, our orientation protocol:
8/8 vs 6/8 there; 3/4 vs 3/4 on Rich." The ETH Zurich/LogicStar null
(arXiv 2602.11988, rev. 2026-09-29) and Khatri null (arXiv
2607.27250) are in the packet's risk section — our Rich result is
consistent with them, not an embarrassment next to them.

## Copilot arm (ledger S16): UNVERIFIABLE

Same 8 NetworkX tasks, Copilot base vs +orientation. 2/8 pairs
completed before the preregistered budget gate stopped the rest;
both pairs concordant passes. Copilot base is 3/3 on every task it
has run in this project (incl. R2, a Claude discordant pair) — the
completed pairs had no headroom. Descriptive, n=2: +orientation
cost/wall ran ABOVE base on both pairs, opposite the Claude
direction. Copilot converts at 3–9× Claude's per-task cost
(1.7–2.0M input tokens on T1/R2 runs, mostly cached, counted at full rate —
upper bounds). Spend $4.63 vs ~$4 cap (one-run overshoot, recorded,
not smoothed). No escapes, no fabrication; all fixes verified in
assigned trees.

## Feedback loop: shipped (ledger S17)

`scripts/run-eval.sh` — one entry point: packaged task → run vs
Claude or Copilot → disk grade → verdict + cost file. Proof run:
nx-t2 package, claude/base, PASS (1/1 grading nodes), 11 turns,
$0.103, 151 s. Carve-outs on the ledger entry: proof used an
existing clone/venv; auto-clone (3m50s one-time, measured) and venv
bootstrap are implemented, not exercised. `docs/feedback-loop.md`
documents the loop step by step, each step labeled automatic /
agent-run / manual as it is today. Branch `phase-2-feedback-loop`
merged into `phase-2` (ledger collision resolved: Copilot = S16,
runner = S17).

## Instruction-debt audit (Anthropic prompt-audit guidance)

Guidance verified first: Anthropic post real (2026-09-08, updated
post-Opus-5.5), six anti-pattern classes verbatim, numbers
confirmed at narrow scope (one support benchmark). One distortion
in the circulating summary: the Lance Martin quote is NOT FOUND
verbatim (he co-authored the post; the command is real).
Our artifacts (2,796 lines): 12 SUSPECT patterns, 0 contradictions.
10 of 12 sit in the two ECC-derived TDD files: unsourced "80%
coverage" constant ×11 locations; "MUST BE USED for all code
changes"; 15-minute calendar re-verification; checkpoint ceremony;
stale Playwright example (fill date 2025-12-31, already past).
4 broken references: `researcher` agent (×5) and `architect`
(canonical: `code-architect`) invoked but nonexistent;
`security-review` skill nonexistent; `tdd-workflow` Step 0 mandates
`scripts/setup-package-manager.js`, which does not exist in the
repo. → Post-demo joint review list.
The orientation artifact itself: ZERO suspect items — a lean variant
would be byte-identical, so the lean A/B was correctly skipped ($0).
Full report: `~/workspace/phase2-prompt-audit-2026-09-30.md`.

## Verification stack (all three completed before this addendum)

- Adversarial refutation pass: 4/4 headline claim groups SURVIVE
  re-derivation from raw artifacts. One DAMAGED line — packet spend
  (port probes $2.78, not <$1) — corrected in the packet.
  `~/workspace/phase2-refutation-2026-09-30.md`.
- Docs fact-check: ZERO packet claims contradicted by official
  docs; suppression trap is documented behavior ("your CLAUDE.md
  files only"); native AGENTS.md load requires Claude ≥ v2.1.277.
  `~/workspace/phase2-docs-factcheck-2026-09-30.md`.
- External signal: ToxicSkills numbers exact vs Snyk primary;
  `npx skills` findings match Vercel README. Wording fixes applied
  to the packet: hook claim scoped to live tests, Copilot precedence
  updated (first-loaded wins agents/skills; LAST-loaded wins MCP),
  custom-agent instruction opt-in noted (CLI v1.0.86+).
  `~/workspace/phase2-external-signal-2026-09-30.md`.

## Spend, updated

Packet total was ≈ $10.5. Extension streams: Rich $1.88; Copilot
A/B $4.63; run-eval proof $0.10; audits/research $0 (no API runs).
Phase 2 all-in ≈ **$17.2** — over the original $15 cap, under
Samuel's 11:11 ET authorization ("spend the rest, I'll add more").
Estimated key balance: ≈ $1 of the $18.23 reported at 07:41 ET.
Estimate, not a provider reading.

## For the 14:00 room

1. CLAUDE.md ruling (Samuel's sway point): delete + version-aware
   guard probe, or keep the bridge. Both defensible; docs support
   either. If delete: smoke test must record the stage machine's
   Claude version (≥ v2.1.277 required for native AGENTS.md load).
2. Narrative (sway point 1, still open): packet recommendation
   stands — Phase 2 leads.
3. Smoke test additions: Claude version on the presentation
   machine + the original five lines (repo root, both CLIs auth,
   one skill end-to-end, `docs/demo-backup/` fallback).
4. D3 (email V1 artifacts) — moot if the build produces a new deck.
