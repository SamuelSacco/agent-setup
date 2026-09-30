---
name: session-harden
description: End-of-session hardening — distill the current session log into maintained wiki notes, update the index, and append to the wiki log. Run before ending any work session.
---

# Session hardening

You are finishing a work session in this workspace. Do this before ending:

1. Open today's session file in `wiki/sessions/` (the one with `status: in-progress`).
2. Read its `## Learned` section. For each durable fact:
   - Search `wiki/notes/` for an existing note on the topic.
   - Update that note (bump `updated`; bump `verified` ONLY if you re-checked the fact) 
     or create a new note following `wiki/data-model.md` (frontmatter, `relates_to`, 
     `[[wikilinks]]`).
3. Update `wiki/index.md` for every note added, renamed, or archived.
4. Append one line to `wiki/log.md`: timestamp, tool, `session`, session filename, outcome.
5. Set the session file's `status:` to `complete` / `partial` / `abandoned` and fill 
   in its `## Outcome` section.
6. Report to the user: notes created/updated, anything left open.

Rules:
- Never edit `wiki/raw/`.
- Never edit past entries in a session's turn log; append corrections.
- A claim without a test stays `verdict: UNVERIFIABLE`. Say so.
