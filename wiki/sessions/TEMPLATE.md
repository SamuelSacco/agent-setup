---
session_id: YYYY-MM-DD-HHMM-tool-slug
tool: claude-code | copilot-cli
model: <model id if known>
started: YYYY-MM-DD HH:MM TZ
status: in-progress | complete | partial | abandoned
intent: <one sentence>
---

# Session: <title>

## Intent
<What the user asked for, in their terms. One or two sentences.>

## Starting state
<What was true when the session began: relevant notes read, repo state, open loops.>

## Turn log
<!-- Append one entry per meaningful step. Never edit past entries. -->

### HH:MM — <step name>
- **Intended:** <what this step was meant to do>
- **Tried:** <command / edit / query actually run>
- **Happened:** <result, including failures verbatim where short>

## Learned
<Durable facts discovered this session. Each should be hardened into wiki/notes/ 
at session end, then referenced here by note id.>

## Outcome
<complete | partial | abandoned — and what remains open.>
