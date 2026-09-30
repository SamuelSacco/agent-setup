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
- [[feedback-loop]] — capture → review → judge → improve; packaged eval runner `scripts/run-eval.sh` (S16)

### References
- [[instruction-files]] — AGENTS.md shared layer, Claude's conditional read, Copilot's no-precedence merge
- [[install-surfaces]] — how capabilities reach each CLI: npx skills, plugin trees, trust gates, MCP keys (P2 W1)

### Claims (with verdicts)
- [[opus-55-prompt-regression]] — UNVERIFIABLE as a general claim; narrow patterns only
- [[claude-advisor]] — PROVEN (with the not-free correction)
- [[copilot-rubber-duck]] — PROVEN (cross-model critic)
- [[specialist-agent-real-code]] — UNVERIFIABLE (same solves as base, +55% turns, P2 W3)
- [[orientation-real-code]] — PROVEN combined n=12 (NetworkX 8/8 vs 6/8; second codebase Rich UNVERIFIABLE 3/4 vs 3/4, no discordant pair)
- [[ecc-ports-invocable]] — PROVEN (all emitted agents/skills/MCP invoked live in both tools; Copilot `--agent` PROVEN for reviewer persona but slow, P2 port verification)

### Decisions
- [[telemetry-storage]] — JSONL/SQLite sidecar; Postgres only if it earns its place
- [[v2-roster]] — V2 default roster from the ECC inventory; data-scientist/ux-ui demoted to optional (P2 W2)

## Archived
<!-- - [[note-id]] — why archived, superseded_by if any -->

## Raw sources
See `wiki/raw/` — immutable; each source should be distilled into notes above.
