# E5 — Context cost of the wiki

**Claim S5:** Excluding archived/stale notes keeps answer quality while 
cutting orientation tokens.

**Pre-registered threshold:** PASS if quality (E2-style probes, 10 questions) 
drops by ≤ 1 correct answer while orientation input tokens drop by ≥ 30% 
on a seeded wiki of ≥ 40 notes (≥ 15 archived/stale).

## Steps
1. Seed `wiki/notes/` with ≥ 40 notes; mark ≥ 15 archived/stale per 
   `data-model.md` retirement rules.
2. Run `scripts/sidecar.sh summary`-style token accounting: measure index + 
   retrieved-note tokens with all notes eligible vs active-only.
3. Answer 10 probe questions under both settings; score blind where possible.

## Heuristic under test
`active-only retrieval` is the default the AGENTS.md orientation describes. 
If quality drops > 1, the retirement rules are too aggressive — loosen them 
and record the change in `data-model.md`.
