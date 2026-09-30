---
id: session-lifecycle
title: Session lifecycle — orient, log, harden
type: procedure
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [telemetry-storage]
sources: []
tags: [process]
---

Every session: (1) orient from `wiki/index.md` + `data-model.md` + recent 
`log.md`; (2) create a session file from `wiki/sessions/TEMPLATE.md` and append 
turn entries (intent / tried / happened, failures included); (3) harden — 
distill durable facts into `wiki/notes/`, update the index, append to 
`wiki/log.md`, close the session with an outcome.

The session log is the audit trail; the notes are the memory. Both tools write 
the same format into the same directories, which is what makes cross-tool 
continuity (eval E2) possible.
