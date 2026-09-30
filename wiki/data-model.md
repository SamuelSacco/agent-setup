# Data Model — Wiki Notes

How every note in `wiki/notes/` is structured, linked, and maintained. 
Agents: read this before creating or editing a note.

## Frontmatter schema

Every note starts with YAML frontmatter:

```yaml
---
id: kebab-case-unique-id          # stable forever; renaming a file keeps the id
title: Human Readable Title
type: concept | decision | procedure | reference | claim | person | project
status: active | stale | archived
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30               # last date the content was checked against reality
relates_to: [other-note-id, another-id]
supersedes: old-note-id            # optional: this note replaces that one
superseded_by: newer-note-id       # optional: set on the OLD note when replaced
sources: [raw/source-file.md]      # raw sources this note draws from
tags: [free, form]
---
```

### Field rules

- **id** — never reuse, never change. Links use ids, not file paths, so notes can move.
- **type** — one of the enum. `claim` notes must carry a verdict (below).
- **status** — `active` (trusted), `stale` (unverified >90 days or failed a lint), 
  `archived` (historical; excluded from default retrieval).
- **verified** — update only when you actually re-checked the content. Never 
  "update" it as a side effect of editing prose.
- **relates_to** — typed graph edges. Every note should link to at least one other 
  note; orphans are a lint failure.
- **supersedes / superseded_by** — when a note replaces another, set both sides in 
  the same edit and set the old note `status: archived`.

### Claim notes carry a verdict

```yaml
verdict: PROVEN | REFUTED | UNVERIFIABLE
evidence: evals/results/<run-id>.md   # the test that produced the verdict
```

A `claim` note without a verdict and evidence link is unfinished work.

## Body conventions

- First paragraph: the note in two sentences. If you can't, the note is two notes.
- Use `[[note-id]]` wikilinks inline; mirror them in `relates_to`.
- Keep notes atomic: one idea per note. Long notes get split, not scrolled.
- Code and commands go in fenced blocks with the language named.

## Lifecycle

```
ingest → note (active) → verified periodically → stale (if unchecked)
       → superseded (replaced) → archived (historical)
```

- **Ingest:** new source in `wiki/raw/` → distill into notes → update `index.md` 
  → append to `log.md`.
- **Query:** answer from notes first; cite note ids. If the answer isn't in the 
  wiki, say so — then offer to ingest the source that would answer it.
- **Lint (weekly or on demand):** find orphans, stale notes, broken `relates_to`, 
  claims without verdicts, notes past their verify-by window. Fix or flag each; 
  append the pass to `log.md`.

## Retirement rules (evaluated, not vibes)

A note is a candidate for archive when **any** hold:
- `verified` older than 180 days **and** zero inbound `relates_to` links.
- Its claim verdict became REFUTED.
- A lint pass finds it duplicated by a newer note (then: supersede, don't delete).

Deletion almost never happens. Archive preserves the audit trail; retrieval 
excludes archived notes by default.
