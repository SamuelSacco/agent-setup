# E2 — Cross-tool session continuity

**Claim S2:** Work started in one tool can be continued by the other from the 
shared session log + wiki, with no copy-paste from the user.

**Pre-registered threshold:** PASS if tool B, cold, correctly answers 4/5 
probe questions whose answers exist ONLY in tool A's session log / notes.

## Steps
1. Tool A: run a small real task (e.g. add a function + test). Ensure the 
   session log and at least one hardened note are written.
2. Tool B (fresh session, same root): ask 5 probes, e.g.:
   - "What did the last session change, and why?"
   - "Which note records the decision made, and what were the alternatives?"
   - "What failed during the last session?"
3. Score: correct = answer matches session log; anything invented = failure.

## Baseline control
Repeat step 2 in a copy of the repo with `wiki/` removed. Expected: tool B 
cannot answer. If it answers anyway, the probes are contaminated — rewrite them.
