---
name: "wiki-lint"
description: "Lint the wiki \u2014 find orphan notes, stale notes, broken relates_to links, claims without verdicts, and index drift. Reports findings and fixes what is safe."
---

# Wiki lint

Audit `wiki/notes/` against `wiki/data-model.md`:

1. **Orphans** — notes with empty `relates_to` and no inbound links from other notes.
2. **Stale** — `verified` older than 90 days, or `updated` older than 180 days with 
   zero inbound links → archive candidate per the data model's retirement rules.
3. **Broken edges** — `relates_to` / `superseded_by` ids that don't resolve to a note.
4. **Unverdicted claims** — `type: claim` notes missing `verdict` or `evidence`.
5. **Index drift** — notes on disk missing from `wiki/index.md`, or index entries 
   pointing at deleted notes.

For each finding: fix it if the fix is mechanical (index entries, one-sided 
supersede links), otherwise flag it in your report with the note id and the rule hit. 
Append one line to `wiki/log.md` for the lint pass. Never delete a note; archive 
with a reason.
