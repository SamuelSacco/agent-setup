# Agent Instructions — Shared Root

You are operating inside a tool-agnostic agent workspace. These instructions apply 
whether you are Claude Code or GitHub Copilot CLI. Tool-specific notes live in 
`docs/tips-claude.md` and `docs/tips-copilot.md`; everything here is shared.

## 1. Orient before acting

At the start of every session:

1. Read `wiki/index.md` — the map of what is known.
2. Read `wiki/data-model.md` — how notes are structured and maintained.
3. Skim the last 3 entries in `wiki/log.md` — what changed recently.
4. State your intent in one sentence before doing work.

Do not skip orientation to "save time." Orientation is what makes the wiki compound.

## 2. Session lifecycle (mandatory)

Every session follows this lifecycle. It is the audit trail and the memory feed.

### Start
- Create `wiki/sessions/<YYYY-MM-DD>-<HHMM>-<tool>-<slug>.md` using the template 
  in `wiki/sessions/TEMPLATE.md`.
- Record: timestamp, tool, model (if known), intent, starting state.

### During
- Append turn entries as you work: what you intended, what you tried, what happened.
- Log failures explicitly — a failed command is data, not embarrassment.
- When you learn something durable, note it in the session under `## Learned`.

### End (hardening)
Before ending, run the hardening step:
1. Extract durable facts from the session into `wiki/notes/` (new or updated notes).
2. Update `wiki/index.md` if notes were added/renamed.
3. Append a summary line to `wiki/log.md`: date, session file, outcome.
4. Mark the session file status: `complete`, `partial`, or `abandoned`.

Raw session logs are never edited after the fact. Corrections go in new entries.

## 3. The wiki

Pattern: immutable raw sources → LLM-maintained linked Markdown → schema (this file).

- `wiki/raw/` — source material. **Never edit.** Agents read, never write.
- `wiki/notes/` — maintained knowledge. Every note has YAML frontmatter (see 
  `wiki/data-model.md`). Notes link to each other with `relates_to` and `[[wikilinks]]`.
- `wiki/index.md` — the map. Keep it current or the system rots.
- `wiki/log.md` — append-only. One line per ingest, session, or lint pass.

### Note lifecycle

- `status: active` — current, trusted.
- `status: stale` — not verified recently; a lint/eval may revive or retire it.
- `status: archived` — kept for history, excluded from default retrieval.
- `superseded_by: <note-id>` — replaced by a newer note; do not cite the old one.

When you cite a note, check its `verified` date. Old + unverified = hypothesis.

## 4. Capabilities (skills, agents, MCP, hooks, plugins)

Capabilities are defined **once** in `canonical/` and installed into both tools by 
`scripts/install.sh`. 

- To use a capability, just use it — the adapters have already placed it where 
  your tool looks for it.
- To *change* a capability, edit `canonical/` and re-run `./scripts/install.sh`. 
  Never edit adapter output by hand; it will be overwritten.
- Specialist agents (e.g. `canonical/agents/backend.md`) are invoked by name.

## 5. Evidence discipline

This workspace treats every claim as unproven until tested.

- When you state a fact about a tool's behavior, label it: **PROVEN** (we ran it), 
  **REFUTED** (we ran it, it failed), or **UNVERIFIABLE** (no test exists yet).
- Verdicts live in `docs/claims-ledger.md`; tests live in `evals/`.
- If a test refutes a note's claim, update the note's `status` and log it. 
  Do not defend stale documentation.

## 6. Telemetry

- Hooks capture structured events (command failures, tool errors, token counts) 
  into the sidecar store — not into your context.
- If asked "what happened in session X," read the session log and the sidecar 
  summary; do not guess from memory.
- Cross-tool continuity: sessions from both tools land in `wiki/sessions/` in the 
  same format, so either tool can read the other's history. Use it.

## 7. Working agreements

- Launch from this root directory, always. The wiki, adapters, and relative 
  paths assume it.
- Prefer small, verified steps. Run the test before claiming the fix.
- Token budget is a real cost: say what a large operation will cost before running it.
- When instructions conflict, this file wins over tool defaults for workspace 
  behavior; the user's direct request wins over this file.
