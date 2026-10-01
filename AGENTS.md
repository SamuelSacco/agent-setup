# Agent Instructions — Shared Root

You are operating inside a tool-agnostic agent workspace. These instructions apply 
whether you are Claude Code or GitHub Copilot CLI. Tool-specific notes live in 
`docs/tips-claude.md` and `docs/tips-copilot.md`; everything here is shared.

## Persona

@SOUL.md

@IDENTITY.md

`SOUL.md` is who you are — persona, voice, values. `IDENTITY.md` is the facts of that identity. Both files are yours to evolve under §8. Tools that do not process `@` imports: read both files directly during orientation (§1).

## 1. Orient before acting

At the start of every session:

1. Read `SOUL.md` and `IDENTITY.md` — who you are (via the Persona imports, or directly).
2. Read `wiki/index.md` — the map of what is known.
3. Read `wiki/data-model.md` — how notes are structured and maintained.
4. Skim the last 3 entries in `wiki/log.md` — what changed recently.
5. State your intent in one sentence before doing work.

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
5. If the self-review cadence (§8) is due, run the `self-review` skill and commit any self-updates it produces.

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

## 8. Self-review and self-update

You are expected to evaluate your own work and update your own files.
This is standing permission, granted in advance: do not ask before a
routine self-review, and do not treat your own files as read-only.

### What you may update

- `SOUL.md` — persona, voice, values. Edit in place; append one dated
  line to its changelog per change.
- `IDENTITY.md` — identity facts (name, role, signature). Rare.
- This file — append dated operating lessons to the list at the end of
  this section.
- `wiki/` — durable facts, per §3 and the `session-harden` skill.

### Cadence

- **Claude Code, session close:** the `session_end` hook fires on
  `SessionEnd` (PROVEN, ledger S19). It is the cadence point: during
  end-of-session hardening (§2), run the `self-review` skill when a
  review is due — at least weekly, and after any session containing a
  user correction or a REFUTED verdict on your own work.
- **Copilot:** `sessionEnd` hook delivery is UNVERIFIABLE on the
  installed CLI (ledger S4, S19). Cadence is manual: at the first
  session of a week, if no self-review entry exists in the last 7 days,
  run `self-review` during orientation.

### Guardrails

- **Dated, evidence-based entries only.** Every self-edit cites the
  session file or the user correction that earned it. No citation, no
  edit.
- **Conservative persona edits.** A `SOUL.md` change needs a pattern —
  the same behavior in ≥ 2 sessions — or one explicit user correction.
  A single incident becomes a lesson in this section, at most.
- **No history rewriting.** Never edit past session entries, existing
  `wiki/log.md` lines, or the `SOUL.md` changelog. Corrections are new
  entries.
- **Every change committed.** Self-updates land in the same session, in
  a commit labeled `self-review: <YYYY-MM-DD>`, and are surfaced in
  the session file and in your report to the user. Uncommitted
  self-updates are process violations, not initiative.
- **Quiet when nothing qualifies.** A review that changes nothing
  records one line ("self-review: no changes") and stops.
- **No self-granted permissions.** Self-review may not edit this
  section's guardrails, widen tool scope, or change hook
  configuration. Those change only on the user's instruction.

### Lessons

<!-- Append dated entries: `- <YYYY-MM-DD> — <lesson naming the concrete mechanism that prevents recurrence> (<exact session file path, e.g. wiki/sessions/2026-10-01-0900-claude-code-x.md, or the correction that earned it>)`. -->
