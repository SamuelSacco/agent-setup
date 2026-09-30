# Claims Ledger

Every claim this system makes, its current verdict, and the evidence.
Updated by eval runs — never by opinion. Verdicts: **PROVEN** / **REFUTED** / 
**UNVERIFIABLE**.

Researched 2026-09-30. Live-tool verdicts pending authentication.

## Tool behavior claims

| # | Claim | Verdict | Evidence |
|---|-------|---------|----------|
| C1 | Claude Code has a `/advisor` command pairing a cheaper model with Opus to save tokens | **PROVEN** with correction — Sonnet drives, Opus advises at decision points; cheaper than Opus-only but each consult costs extra Opus-rate tokens; not token-neutral | research: hidden_files/research/claims-tips.md |
| C2 | GitHub Copilot CLI has a "rubber duck" feature | **PROVEN** — built-in cross-model critic agent (Claude↔GPT); auto-consulted on non-trivial work; `/rubber-duck` to invoke | research: claims-tips.md |
| C3 | Opus 5.5 makes older prompts behave worse | **UNVERIFIABLE** as a general claim; narrow patterns partially supported (prefill removal, effort default) | research: opus-55-prompt-claim.md |
| C4 | Current discovery/precedence of AGENTS.md vs CLAUDE.md vs muse-instructions | **PROVEN** (docs) — AGENTS.md is the shared layer; Claude Code reads it natively since v2.1.277 only when no CLAUDE.md is present; `@AGENTS.md` import is the robust bridge; Copilot CLI combines files with no defined precedence | research: instructions-files.md |

## System claims (ours — must earn PROVEN)

| # | Claim | Verdict | Evidence |
|---|-------|---------|----------|
| S1 | One install (`scripts/install.sh`) makes a canonical skill discoverable in BOTH tools | PARTIAL — Copilot discovery PROVEN unauthenticated; Claude discovery + any invocation UNVERIFIABLE until auth | evals/results/2026-09-30-E1-partial.md |
| S2 | A session in tool A is continuable by tool B from the shared session log + wiki | UNVERIFIABLE | evals/tasks/E2-cross-tool-continuity.md |
| S3 | Wiki orientation improves task success vs no-wiki baseline | UNVERIFIABLE | evals/tasks/E3-wiki-value.md |
| S4 | The failure-capture hook records structured failure events to the sidecar | UNVERIFIABLE (sidecar itself tested locally) | evals/tasks/E4-failure-capture.md |
| S5 | Excluding archived/stale notes holds answer quality while cutting context tokens | PARTIAL — token axis: 38% cut on seeded wiki (≥30% threshold met); quality axis UNVERIFIABLE until auth | evals/results/2026-09-30-E5-partial.md |
| S6 | Shared specialist agents behave consistently across both tools on the same task | UNVERIFIABLE | evals/tasks/E6-agent-parity.md |

## How a verdict changes

1. Run the eval in `evals/tasks/` exactly as written (thresholds pre-registered).
2. Write results to `evals/results/<date>-<eval-id>.md`.
3. Update this ledger + the matching `type: claim` wiki note in the same change.
4. A REFUTED system claim is not hidden — it drives a fix or a removal.
