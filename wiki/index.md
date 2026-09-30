# Wiki Index

The map of maintained knowledge. Agents: read this first, keep it current.

## How to use this index
- Find notes by topic below, or search `relates_to` edges from a note you have.
- Archived notes are listed separately and excluded from default retrieval.
- A note missing from this index is invisible — if you create one, add it here.

## Notes by type

### Concepts
<!-- - [[note-id]] — one-line description -->

### Decisions

### Procedures
- [[session-lifecycle]] — orient → log → harden; the audit trail both tools share
- [[instruction-debt]] — canonical prompt-debt fixes 2026-09-30: broken references rewired, 80% defined once as heuristic default, rituals trimmed to mechanism
- [[feedback-loop]] — capture → review → judge → improve; packaged eval runner `scripts/run-eval.sh` (S17)

### References
- [[instruction-files]] — AGENTS.md shared layer, Claude's conditional read, Copilot's no-precedence merge
- [[install-surfaces]] — how capabilities reach each CLI: npx skills, plugin trees, trust gates, MCP keys (P2 W1)

### Claims (with verdicts)
- [[opus-55-prompt-regression]] — UNVERIFIABLE as a general claim; narrow patterns only
- [[claude-advisor]] — PROVEN (with the not-free correction)
- [[copilot-rubber-duck]] — PROVEN (cross-model critic)
- [[specialist-agent-real-code]] — UNVERIFIABLE (same solves as base, +55% turns, P2 W3)
<<<<<<< HEAD
- [[orientation-real-code]] — PROVEN combined n=12 (NetworkX 8/8 vs 6/8; second codebase Rich UNVERIFIABLE 3/4 vs 3/4, no discordant pair)
- [[claude-opus-critique]] — pre-merge red-team (Opus 5.5): S12/S4 BLOCKERs, S14 PARTIAL, S5/S6b corrected; adapters.py drops agent tool restrictions
=======
- [[orientation-real-code]] — PROVEN combined n=12 at Haiku tier (NetworkX 8/8 vs 6/8; second codebase Rich UNVERIFIABLE 3/4 vs 3/4, no discordant pair); model-tier test on claude-opus-5-5: UNVERIFIABLE, zero discordant pairs on either codebase (S18)
>>>>>>> origin/exp/bigmodel-orientation
- [[ecc-ports-invocable]] — PROVEN (all emitted agents/skills/MCP invoked live in both tools; Copilot `--agent` PROVEN for reviewer persona but slow, P2 port verification)
- [[session-end-hook]] — PROVEN trigger, Claude only (SessionEnd hook fires headless 2/2 + shipped wiring; cleanup skill not built; S18)
- [[skill-import-pinning]] — PROVEN prototype (hash-pin + audit-check skill import; tampered skill refused in demo; S19)

### Decisions
- [[telemetry-storage]] — JSONL/SQLite sidecar; Postgres only if it earns its place
- [[v2-roster]] — roster of record: the 12 canonical agents on disk, all installed, no tiers (X20 decision 2026-09-30 in the note's dated correction); W2 7-default and packet 6+2 rosters retired as shipped-state descriptions; task-runner/evaluator not built

## Archived
<!-- - [[note-id]] — why archived, superseded_by if any -->

## Raw sources
See `wiki/raw/` — immutable; each source should be distilled into notes above.
