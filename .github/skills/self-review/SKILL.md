---
name: self-review
description: Periodic self-evaluation — rate recent work on 5 axes from session logs and telemetry, route what you learned to the right file (lessons to AGENTS.md, persona to SOUL.md, facts to the wiki), and commit the update. Run at session close (SessionEnd cadence) or weekly.
---

# Self-review

You are evaluating your own recent work and updating your own files.
This is a standing, encouraged part of the job (`AGENTS.md` §8) — not an
exception and not self-promotion. Output is small, dated, and committed,
or it did not happen.

## 1. Gather inputs (read, don't recall)

- The session files in `wiki/sessions/` since the last self-review
  (check `git log --oneline -- wiki/sessions/` if unsure).
- `scripts/sidecar.sh summary` — failure counts and session-end events
  from the telemetry sidecar.
- `git log --oneline -20` — what actually landed.
- The current `SOUL.md` changelog — do not re-litigate settled entries.

If there are no new sessions since the last review, stop. Record
nothing. A quiet review is a valid review.

## 2. Self-rate on 5 axes

Rate each axis 1–5. Every rating cites a concrete instance from the
inputs (session file + what happened). No citation, no rating.

| Axis | Question |
|---|---|
| Accuracy | Were my factual claims and verdicts right when checked? |
| Completeness | Did I finish what the session set out to do, or silently drop parts? |
| Clarity | Could the user (or the next session) act on my output without re-reading the transcript? |
| Actionability | Did my output end in done work and named next steps, or in advice handed back? |
| Evidence discipline | Did every claim carry PROVEN / REFUTED / UNVERIFIABLE with disk evidence behind it? |

Any axis ≤ 2 requires a routed lesson (step 3) naming the fix, or an
explicit note why no fix exists. Ratings go in the review entry (step 4),
not in `SOUL.md`.

## 3. Route each finding to exactly one file

| Finding | Goes to |
|---|---|
| Operating lesson (how to do the work) | `AGENTS.md` — append a dated entry to the lessons in §8 |
| Persona-level pattern (how you carry yourself) | `SOUL.md` — edit in place + one dated changelog line citing the evidence |
| Identity fact (name, role, signature) | `IDENTITY.md` — user corrections only, or ratified proposals |
| Durable fact about the codebase / tools / world | `wiki/notes/` via the session-harden flow |
| Nothing genuine | Nowhere. Stop. |

Persona bar: a `SOUL.md` edit needs a pattern — the same behavior in
≥ 2 sessions, or one explicit user correction. A single incident is a
lesson (`AGENTS.md`) at most, never a persona edit.

**Mechanism rule.** A lesson drawn from a friction instance must name
the concrete mechanism that prevents recurrence — the exact command,
directory, path, or setting. "Read errors before retrying" alone does
not conform; "run the eval suite from `demo/` — from the repo root it
collects zero tests" does. If a session's `## Learned` states a durable
fact that is not yet in `wiki/notes/`, route the fact itself, with its
mechanism intact, to a note or a lesson — never let it survive only as
a generic paraphrase. (Added after the S25 behavior probe: the first
live run routed three generic discipline lessons and dropped the
seeded working-directory fact.)

## 4. Write the review entry

Append to today's session file, or create
`wiki/sessions/<YYYY-MM-DD>-<HHMM>-<tool>-self-review.md` from the
template, containing: the 5 ratings with citations, every file changed
(and why), and anything deliberately not changed. Append one line to
`wiki/log.md`.

## 5. Commit

One commit for the whole review: `self-review: <YYYY-MM-DD>`. Every
self-change is a diff the user can read and revert. Uncommitted
self-updates are process violations, not initiative.

Before committing, check the diff against this list — every item, or
the review is not conformant:

- Every `AGENTS.md` lesson is dated, names its mechanism (rule above),
  and ends with the exact session-file path in parentheses:
  `(wiki/sessions/<file>.md)`. A description like "(seeded session)"
  is not a citation.
- Every axis rated ≤ 2 has a routed lesson, or an explicit note why
  no fix exists.
- `wiki/log.md` has exactly one new line for this review.
- No persona file (`SOUL.md`, `IDENTITY.md`) changed without meeting
  its bar in step 3.

## Guardrails

- Never rewrite history: session logs are append-only; corrections are
  new entries. `wiki/raw/` is never edited.
- Never use self-review to grant yourself permissions, widen your tool
  scope, or edit the guardrails in `AGENTS.md` §8. Those change only on
  the user's instruction.
- Redact before recording: no credentials, tokens, or raw payloads in
  any self-review artifact (the sidecar allowlist rule applies to you
  too).
- Report the review to the user in the session report: ratings, files
  changed, commit hash. If nothing changed, one line: "self-review:
  no changes."
