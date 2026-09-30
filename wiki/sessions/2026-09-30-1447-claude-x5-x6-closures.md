---
session_id: 2026-09-30-1447-claude-x5-x6-closures
tool: claude-code
model: Muse Spark (subagent)
started: 2026-09-30 14:47 EDT
status: complete
intent: Close backlog items X5 (SessionEnd cleanup-hook probe) and X6 (hash-pin + audit-check skill-import prototype) with disk-verified verdicts; branch exp/x5-x6-closures off phase-2.
---

# Session: Backlog closures X5 + X6

## Intent
Two cheap, decisive backlog items from `docs/experiments-backlog.md`. X5: the
talk close says cleanup runs automatically at session close via hook —
UNPROVEN; test whether a Claude Code session-end hook fires in headless
(`claude -p`) runs. X6: the packet's only forward-looking claim (nobody
enforces snapshot + hash-pin + audit-check on skill import) — UNBUILT; build
the smallest real prototype and demo it against one clean and one tampered
skill. API budget: $0.75 hard cap for the whole task (X6 is $0 API).

## Starting state
- Fresh clone of `SamuelSacco/agent-setup` at `~/workspace/p3/x5x6`,
  branch `exp/x5-x6-closures` off phase-2 head `5ffbcbd` (wave-1 merges in).
- Git identity set to the repo convention (`Helm <helm@localhost>`); a plain
  `git clone https://…` hung on a credential prompt (no credential helper
  configured) — cloned via `gh repo clone` instead.
- Claude Code on this machine: **2.1.285** (`~/workspace/tools/bin/claude`).
- Read per AGENTS.md §1: wiki/index.md, wiki/data-model.md, last 3 log
  entries, backlog X5/X6, claims ledger (next free system ids: S18, S19),
  `scripts/adapters.py` (hook translation), `scripts/sidecar.sh`.

## Turn log

### 14:47 — Setup + orientation
- **Intended:** clone, branch, read rules/backlog/ledger/adapter.
- **Tried:** `gh repo clone` after the https clone hung on credentials;
  reads listed above.
- **Happened:** branch ready at phase-2 head `5ffbcbd`. Findings that shape
  the work: `install_hooks()` in adapters.py currently maps *every*
  canonical hook to Claude `PostToolUseFailure` / Copilot
  `postToolUseFailure` regardless of the canonical `event` field — wiring a
  session-end hook properly means generalizing that map. Canonical hooks
  are single JSON files under `canonical/hooks/` (name/event/action.command).
  Skills are single `.md` files under `canonical/skills/` (frontmatter
  name/description). Sidecar appends JSONL events to `wiki/telemetry/`.

### 14:49 — Preregistration written before any run
- **Intended:** fix decision rules and audit policy on disk before executing.
- **Tried:** wrote the preregistration sections of
  `evals/results/2026-09-30-X5-sessionend-probe.md` and
  `evals/results/2026-09-30-X6-hashpin-prototype.md`.
- **Happened:** rules fixed (see those files). No probe run or demo has
  executed yet at the time of writing.

### 14:51 — X5 probe runs (scratch)
- **Intended:** 2 headless `claude -p` runs against a scratch
  `.claude/settings.json` registering a `SessionEnd` marker hook.
- **Tried:** Haiku model, `--output-format json`, marker hook appends
  timestamp + raw payload to `marker.log`.
- **Happened:** marker written by the hook alone in **both** runs; each
  payload's `session_id` matched the CLI-reported session, ids distinct,
  `hook_event_name: "SessionEnd"`, `reason: "other"`. BUT both model
  turns returned `Credit balance is too low` (metered $0) — the API
  key's balance was exhausted at probe time. Sessions still terminated
  through the normal lifecycle, which is the event under test; logged
  as an explicit caveat in the results doc, not hidden.

### 14:53 — X5 shipped wiring + confirmation run
- **Intended:** wire the minimal mechanism into the repo and prove the
  shipped path, per the task's PROVEN branch.
- **Tried:** added `canonical/hooks/session-end.json` (event
  `session_end`); generalized `install_hooks()` in
  `scripts/adapters.py` to `HOOK_EVENT_MAP` (canonical → Claude +
  Copilot event names; `tool_failure` output byte-identical); added
  `record-session-end` to `scripts/sidecar.sh`; re-ran `install.sh`;
  one headless run from the repo root.
- **Happened:** `.claude/settings.json` gained `SessionEnd` →
  `./scripts/sidecar.sh record-session-end`; `.github/hooks/session-end.json`
  emitted. The run appended a `kind: "session_end"` line to
  `wiki/telemetry/events.jsonl` with matching session id. Trigger
  PROVEN end-to-end through the exact shipped artifacts.

### 14:55 — X6 prototype + demo
- **Intended:** build `scripts/import_skill.py` (audit → import →
  SHA-256 pin; `verify` re-hashes) and run the preregistered demo.
- **Tried:** demo in scratch root: clean skill import; tampered skill
  (planted override + pipe-to-shell + credential-exfiltration lines)
  import; post-import edit + `verify`; `--force` restore + `verify`.
- **Happened:** all four steps as preregistered — clean import pinned
  (hash matches independent `sha256sum`); tampered REFUSED (exit 3,
  4 critical findings, no file, no pin); post-import edit → MISMATCH
  (exit 1); restore → verify OK. Full transcript (payload lines
  redacted to bracketed markers) in the results doc.

### 14:58 — Documentation + hardening
- **Intended:** verdicts in every surface the repo requires.
- **Tried:** results docs completed; ledger gained S18 + S19; backlog
  X5/X6 statuses updated; dated update notes appended to the packet;
  claim notes [[session-end-hook]] + [[skill-import-pinning]] created
  and indexed; this session hardened; log line appended.
- **Happened:** see Outcome.

## Learned
- Claude Code 2.1.285 fires `SessionEnd` hooks at the end of headless
  (`-p`) sessions — including sessions whose model turn failed. A
  session-close trigger therefore does not depend on turn success.
  → [[session-end-hook]]
- The adapter's hook translation was a hard-coded single-event map;
  generalizing it to a canonical→per-tool event table kept the
  existing hook's emitted bytes identical while making new events a
  one-line addition. → session record only (adapter change itself is
  the artifact).
- A pattern-list audit with an explicit refuse/flag policy is enough
  to demonstrate the import-enforcement shape and catch a planted
  tamper — and its limits (named classes only) are just as explicit.
  → [[skill-import-pinning]]
- A plain `git clone https://…` can hang silently in this sandbox (no
  git credential helper); `gh repo clone` is the reliable path.

## Outcome
complete — X5 verdict PROVEN (trigger, Claude; S18), X6 prototype
built and demo-verified (S19). Task API spend: **$0.00** of the $0.75
cap (every model turn was blocked on the exhausted key before billing;
X6 is local by design). Open, deliberately: a confirmatory X5 re-run
on a successful turn once credit is restored; a real cleanup procedure
on the session-end trigger; Copilot session-end remains UNVERIFIABLE.
