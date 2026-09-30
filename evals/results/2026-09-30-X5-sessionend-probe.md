# X5 — SessionEnd cleanup-hook probe (Claude Code)

Backlog: `docs/experiments-backlog.md` X5.
Claim under test: "cleanup runs automatically at session close via hook"
(talk close, `docs/morning-review-2026-09-30.md`) — status before this
probe: **UNPROVEN** in both tools. This probe covers **Claude Code only**;
the Copilot side stays UNPROVEN (its installed-CLI hook surface is already
REFUTED for failure hooks, ledger S4).

## Preregistration (written 2026-09-30 14:49 EDT, before any run)

- Tool/version: Claude Code **2.1.285** (`claude --version`, this sandbox).
- Mechanism under test: a hook registered on the session-end event in a
  scratch project's `.claude/settings.json`. First choice: the `SessionEnd`
  event. If 2.1.285 does not fire `SessionEnd` headless, fall back to the
  closest real session-end event the version exposes and name it.
- Hook action (the marker + minimal cleanup stub): append one line
  `"<UTC timestamp> <raw hook payload JSON>"` to `marker.log` in the
  scratch dir. The payload carries `session_id`, so the marker records
  timestamp + session id as required.
- Runs: 2 headless runs, `claude -p "Reply with exactly the word: ok"`,
  model `claude-haiku-4-5-20251001`, `--output-format json` (cost read from
  `total_cost_usd`). Scratch dir:
  `~/workspace/p3/x5x6-scratch/sessionend/`.
- Decision rule (fixed in advance):
  - **PROVEN** — the marker appears from the hook alone in both runs
    (2 distinct session ids, no manual step between session end and check).
  - **REFUTED** — the event never fires headless across both runs.
  - **PARTIAL** — it fires only interactively, or only via a different
    event than `SessionEnd` (named in the verdict).
- If PROVEN via a real event: wire the minimal version into the repo —
  a canonical hook definition under `canonical/hooks/`, the adapter event
  map generalized so `install.sh` emits it, and a sidecar
  `record-session-end` action (marker/cleanup stub: appends the session-end
  event to the sidecar store). No full cleanup skill will be invented; the
  claim under test is the trigger mechanism.
- Budget: ≤ $0.20 of the task's $0.75 cap.

## Runs

Scratch install as preregistered (`SessionEnd`, matcher `*`, hook appends
timestamp + raw payload to `marker.log`). Two headless runs, back to back:

| Run | CLI session_id | Marker line (verbatim) | Metered cost |
|-----|----------------|------------------------|--------------|
| 1 | `7511c826-33ff-4bd5-bcd6-1df05691526b` | `2026-09-30T18:48:05Z {"session_id":"7511c826-…","transcript_path":"…/7511c826-….jsonl","cwd":"…/x5x6-scratch/sessionend","prompt_id":"347045fc-…","hook_event_name":"SessionEnd","reason":"other"}` | $0 |
| 2 | `2d4e8232-0daa-4d0f-9daa-bbbeb624a4c2` | `2026-09-30T18:48:38Z {"session_id":"2d4e8232-…", … "hook_event_name":"SessionEnd","reason":"other"}` | $0 |

Each marker's `session_id` matches the session id the CLI reported for
that run; the two ids are distinct; nothing but the hook wrote the file.

**Shipped-wiring confirmation (1 further run):** after wiring the repo
(canonical hook + adapter map + sidecar action, below), one headless run
from the repo root appended via the exact shipped path
(`.claude/settings.json` → `./scripts/sidecar.sh record-session-end`):

```
{"ts":"2026-09-30T18:49:46Z","kind":"session_end","payload":{"session_id":"66944e45-581f-4b4e-8f8b-921050596e90", … "hook_event_name":"SessionEnd","reason":"other"}}
```

in `wiki/telemetry/events.jsonl`, session id again matching the CLI's.

**Caveat — the model turns did not succeed.** All three sessions returned
`Credit balance is too low` (metered cost $0): the API key's balance was
exhausted at probe time. The sessions still started, ran their lifecycle,
and terminated normally — which is the event under test. `SessionEnd`
fired in every case, including for an error-terminated session (arguably
the case a cleanup trigger matters most). A confirmatory re-run on a
successful turn is cheap and worth doing when credit is restored, but the
preregistered decision rule (marker from the hook alone, 2 headless runs,
distinct session ids) does not condition on turn success.

## Verdict

**PROVEN** (Claude Code 2.1.285, headless) — the `SessionEnd` hook event
fires at the end of `claude -p` sessions, 2/2 in the scratch probe and
1/1 through the shipped wiring, with no manual step. Scoped precisely:

- PROVEN: the *trigger mechanism* — a session-end hook runs automatically
  at session close in Claude Code, headless included.
- NOT claimed: a cleanup *skill* runs at close. No cleanup skill exists;
  the wired action is the minimal stub below. Building the actual cleanup
  procedure on this trigger is future work.
- Copilot: unchanged — UNVERIFIED (installed CLI has no hook loader, S4).

Wired into the repo in this change:

- `canonical/hooks/session-end.json` — canonical `session_end` event →
  `./scripts/sidecar.sh record-session-end`.
- `scripts/adapters.py` — `install_hooks()` generalized to
  `HOOK_EVENT_MAP` (canonical event → Claude + Copilot event names);
  `tool_failure` output is byte-identical to before.
- `scripts/sidecar.sh` — new `record-session-end` action: appends a
  `kind: "session_end"` JSONL event to the sidecar store. That record is
  the cleanup stub: the place session-close steps attach.
- Regenerated: `.claude/settings.json` (gains `SessionEnd`),
  `.github/hooks/session-end.json` (emitted for when Copilot ships a
  loader).

## Spend

$0.00 metered (all runs blocked on the exhausted key before any billable
turn; cap for this item was ~$0.20 of the task's $0.75).
