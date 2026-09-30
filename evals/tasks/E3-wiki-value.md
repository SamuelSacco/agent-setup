# E3 — Does the wiki actually help?

**Claim S3:** Orienting from the wiki improves task outcomes vs a no-wiki baseline.

**Pre-registered threshold:** PASS if the wiki arm beats the baseline arm on 
the rubric below across 5 matched tasks, with ≤ 25% mean token overhead.

## Design
- 5 small realistic tasks (bugfix, extend-a-feature, answer-from-history, 
  refactor-per-convention, find-the-decision).
- Arm A: full workspace (AGENTS.md orientation + wiki).
- Arm B: identical repo with `wiki/notes/` emptied and orientation skipped.
- Same model, same tool, interleaved order to wash out drift.

## Rubric (per task)
- Correct outcome (0/1)
- Steps/turns to completion
- Input tokens (tool-reported where available; else chars/4 estimate, labeled)
- Convention violations (0-n)

## Failure mode this catches
A wiki that costs 25% more tokens and changes nothing gets its orientation 
step redesigned or dropped. That is a legitimate result.
