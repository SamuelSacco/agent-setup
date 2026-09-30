# Claims Ledger

Every claim this system makes, its current verdict, and the evidence.
Updated by eval runs — never by opinion. Verdicts: **PROVEN** / **REFUTED** / 
**UNVERIFIABLE**.

Researched and live-tested 2026-09-30 (Claude Code + Copilot CLI, both
authenticated; see evals/results/).

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
| S1 | One install (`scripts/install.sh`) makes a canonical skill discoverable in BOTH tools | **PROVEN** 2026-09-30 — Copilot invoked `session-harden` by name and executed its body; Claude Code did the same in a fresh scratch install ($0.042 run). Both read the real canonical procedure; neither invented facts | evals/results/2026-09-30-E1-partial.md; 2026-09-30-E1-claude.md |
| S2 | A session in tool A is continuable by tool B from the shared session log + wiki | **PROVEN** 2026-09-30 — Claude (cold) answered 5/5 probes from a Copilot session record, incl. correctly reporting the decision was recorded in NO note; baseline with wiki/ removed: 5/5 "not recorded", nothing invented | evals/results/2026-09-30-E2.md |
| S3 | Wiki orientation improves task success vs no-wiki baseline | UNVERIFIABLE | evals/tasks/E3-wiki-value.md |
| S4 | The failure-capture hook records structured failure events to the sidecar | **PARTIAL** 2026-09-30 — Claude: PROVEN 5/5 after adapter fix (canonical `tool_failure` → `PostToolUseFailure`; `PostToolUse` is success-only). Copilot: REFUTED on installed CLI v1.0.89 — binary contains no hook loader; 0/5 | evals/results/2026-09-30-E4.md |
| S5 | Excluding archived/stale notes holds answer quality while cutting context tokens | PARTIAL — token axis: 38% cut on seeded wiki (≥30% threshold met); quality axis UNVERIFIABLE until auth | evals/results/2026-09-30-E5-partial.md |
| S6 | Shared specialist agents behave consistently across both tools on the same task | UNVERIFIABLE | evals/tasks/E6-agent-parity.md |
| S7 | One Anthropic credential drives BOTH harnesses (model constant, harness the only variable) | **PROVEN** 2026-09-30 — Copilot CLI BYOK (`COPILOT_PROVIDER_TYPE=anthropic`) ran on the stored Anthropic key; footer showed tokens with no AI Credits line (GitHub-hosted runs meter credits). Claude Code uses the same key via apiKeyHelper | evals/results/2026-09-30-byok-probe.md |

## How a verdict changes

1. Run the eval in `evals/tasks/` exactly as written (thresholds pre-registered).
2. Write results to `evals/results/<date>-<eval-id>.md`.
3. Update this ledger + the matching `type: claim` wiki note in the same change.
4. A REFUTED system claim is not hidden — it drives a fix or a removal.
