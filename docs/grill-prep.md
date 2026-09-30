# Grill Prep — anticipated hard questions

For the 2–4pm rehearsal. Each answer: claim, verdict, evidence. If you don't 
know, the correct answer is "UNVERIFIABLE — here's the test that would decide it."

## "Isn't this just ECC / a dotfiles repo?"
ECC-style suites are robust and invasive. This is the slim version: one canonical 
layer, two adapters, a wiki, an eval ledger. The difference isn't features — it's 
that every claim here carries a verdict and a test. If a piece doesn't beat its 
baseline in E3/E5, it gets cut.

## "Why not just use AGENTS.md and skip the adapters?"
AGENTS.md unifies instruction *text* only (PROVEN, research brief). It does not 
standardize skills layout, agents, MCP config, hooks, or enforcement — those 
differ per tool today. Adapters exist for exactly the non-unified residue.

## "Does Claude Code even read AGENTS.md?"
Yes since v2.1.277 (2026-09-18) — conditionally: only when no CLAUDE.md exists in 
cwd or above. We use `CLAUDE.md` = `@AGENTS.md` import, Anthropic's recommended 
bridge. "Claude never reads AGENTS.md" is REFUTED (outdated).

## "Which wins, CLAUDE.md or muse-instructions?"
Wrong frame per surface: github.com has a precedence list; Copilot CLI *combines* 
with no defined order; Claude concatenates with its own modes. Our rule: one 
source of truth (AGENTS.md), thin per-tool pointers, no conflicts to referee.

## "Is /advisor actually cheaper?"
Cheaper than Opus-as-main; not free. Each consult bills at Opus rates and 
re-reads the full transcript. On short tasks it's overhead — Anthropic's own 
docs say so. We present it as such.

## "Did Opus 5.5 break old prompts?"
UNVERIFIABLE as stated; the viral post making the claim contains errors (XML is 
not deprecated). Real changes: prefills removed, `effort` unset changes budgets. 
Retuning ≠ regression.

## "Why not Postgres for telemetry?"
Single writer, low volume, file-native consumers. JSONL + SQLite covers it. 
Postgres earns its place with concurrent writers or cross-machine queries. 
Decision recorded in wiki note [[telemetry-storage]].

## "Does the wiki actually help, or is it token bloat?"
That's E3 (wiki vs no-wiki on 5 matched tasks, ≤25% token overhead threshold) 
and E5 (archived-note exclusion, ≥30% token cut for ≤1 quality drop). Until 
they run: UNVERIFIABLE — and the design includes the cut criterion if it fails.

## "How is this different from just using one tool?"
It isn't an argument against one tool. It's insurance + leverage: shared memory 
means no lock-in of accumulated knowledge, and each tool's unique features 
(/advisor, rubber duck) stay available without splitting the knowledge base.

## "What breaks first at org scale?"
Three honest candidates: (1) adapter drift when a vendor changes formats — 
mitigated by E1/E6 re-runs on upgrade; (2) wiki rot — mitigated by lint + 
retirement rules, measured by E5; (3) instruction conflicts in Copilot's 
no-precedence merge — mitigated by the single-source rule.

## "What did you actually verify vs assert?"
Point at `docs/claims-ledger.md`. Tool claims: researched to primary sources 
(PROVEN/REFUTED/UNVERIFIABLE). System claims: UNVERIFIABLE until the evals run 
live — the demo runs E1/E2/E4 in front of the audience.
