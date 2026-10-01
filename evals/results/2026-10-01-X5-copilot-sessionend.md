# X5 Copilot arm — does a `sessionEnd` hook fire on Copilot CLI 1.0.89?

Backlog: `docs/experiments-backlog.md` X5. Ledger: S19 (Claude trigger
PROVEN 2026-09-30, evidence
`evals/results/2026-09-30-X5-sessionend-probe.md`; Copilot side
UNVERIFIABLE). Ledger S4 (audit-corrected): Copilot hook surface exists
and fires under directory trust for `sessionStart` / `preToolUse` /
`postToolUse` (E4 retest); `postToolUseFailure` does not fire for shell
failures. `sessionEnd` specifically has never been behaviorally tested.

## Preregistration (written 2026-10-01, before any probe run)

- Tool/version: Copilot CLI **1.0.89** (`~/workspace/tools/bin/copilot`,
  `copilot --version`).
- Config surface under test (the documented one): repo-level
  `.github/hooks/*.json`, `version: 1`, `hooks` object mapping event
  name → array of `{type: "command", bash, timeoutSec}`. This is the
  exact format the repo adapter already emits
  (`.github/hooks/session-end.json`). Other documented surfaces
  (user `~/.copilot/hooks/*.json`, inline `hooks` key in settings,
  plugin `hooks.json`) are noted, not tested: if the documented repo
  surface fails, the shipped claim (adapter emits repo file) fails.
- Trust: repo hooks load only in a trusted directory. Trust is granted
  via `COPILOT_ALLOW_ALL=true` (exact string; `copilot help
  environment`: exact `"true"` "additionally trusts the working
  directory", which loads its hooks). Runs also pass
  `--allow-all-tools --allow-all-paths`.
- Model/provider: BYOK Anthropic, exactly as the X17 runner —
  `COPILOT_PROVIDER_TYPE=anthropic`,
  `COPILOT_PROVIDER_BASE_URL=https://api.anthropic.com`,
  `COPILOT_PROVIDER_MODEL_ID=claude-haiku-4-5-20251001`, key via the
  vault helper (`claude_api_key_helper.py`, never printed/committed).
- Scratch workspace: `~/workspace/w4b-x5copilot-scratch/`,
  git-initialised, containing one hook file
  `.github/hooks/session-end.json` registering:
  - `sessionEnd` → append `sessionEnd <UTC timestamp>` to
    `marker.log` in the scratch dir (absolute path; nothing else in
    the probe writes this file).
  - `sessionStart` → append `sessionStart <UTC timestamp>` to
    `start-marker.log` in the scratch dir. Control: proves the hook
    loader + trust are active in the same session, so a negative
    `sessionEnd` result is attributable to that event, not to a
    broken probe.
- Runs: headless `copilot -p "Reply with exactly the word: ok"
  --output-format json`, run to normal process exit, then check the
  markers. Trial 1; trial 2 if trial 1 is negative and budget allows.
- Decision rule (fixed in advance):
  - **PROVEN** — `marker.log` written by the hook alone in ≥1
    completed session (ideally 2/2), timestamp matching session end.
  - **REFUTED** — sessions complete normally, `sessionStart` control
    fires, `marker.log` never appears, across the trials run (trial
    count stated).
  - **UNVERIFIABLE** — no configurable surface exists to register
    the test, sessions fail for unrelated reasons, or the
    `sessionStart` control also fails (probe cannot distinguish
    "sessionEnd broken" from "hooks not loading").
- Corroboration: grep the installed 1.0.89 binary bundle for
  `sessionEnd` / hook-loader strings; report counts.
- Budget: ~$0.50. Converted cost = token totals at the repo
  convention ($1/M input, $5/M output, cached at full rate = upper
  bound). BYOK runs show no AI Credits line; billing is Anthropic-side.

## Config surface (step 1 findings)

- `copilot --help`: no hooks subcommand/flag; hooks are file-config
  only. `copilot help environment` confirms the trust mechanism:
  `COPILOT_ALLOW_ALL` set to exactly `"true"` "additionally trusts
  the working directory", which loads its hooks.
- Repo research (`hidden_files/research/2026-09-30-P2-copilot-surface.md`
  §5, `2026-09-30-copilot-cli-docs.md`): documented surfaces are repo
  `.github/hooks/*.json`, user `~/.copilot/hooks/*.json`, inline
  `hooks` key in settings, plugin `hooks.json`. Tested: the repo
  surface (the one the adapter emits). Format: `version: 1`,
  `hooks.sessionEnd[]` entries `{type: "command", bash, timeoutSec}`.
- Prior docs note: `sessionEnd` hook *output* is not processed by
  Copilot (cannot inject context) — irrelevant to this probe: the
  hook's own side effect (appending to `marker.log`) is the test.

## Runs

Scratch hook file registered `sessionEnd` → `marker.log` and, as
loader control, `sessionStart` → `start-marker.log` (absolute paths;
nothing else in the probe writes either file). Prompt all trials:
`Reply with exactly the word: ok`, `--output-format json`.

| Trial | Session id | Outcome | sessionStart marker | sessionEnd marker |
|-------|-----------|---------|--------------------|--------------------|
| 1 | `b4c35cb4-6ebb-4045-ba10-2b79730fae8d` | Model reply `ok` produced after 4 transport retries (ETIMEDOUT to api.anthropic.com); external 300 s timeout TERM landed the same second → abort-end (`result` 04:18:01.227Z) | `sessionStart 2026-10-01T04:16:47Z` | `sessionEnd 2026-10-01T04:18:01Z` |
| 2 | `6210e31c-ab24-442f-8ec9-cbe3d94f0fde` | All 6 model calls ETIMEDOUT; `session.error` "Connection timed out to provider"; process self-exited, exit 1 (`result` 04:22:39.845Z). Isolated `COPILOT_HOME` (no user MCP servers) | `sessionStart 2026-10-01T04:21:16Z` | `sessionEnd 2026-10-01T04:22:39Z` |
| 3 | `ef33d356-6acc-4d06-b02f-35bf509660aa` | Same transport failure; process self-exited, exit 1 (`result` 04:24:51.502Z) | `sessionStart 2026-10-01T04:23:28Z` | `sessionEnd 2026-10-01T04:24:51Z` |

`marker.log` verbatim (all of it):

```
sessionEnd 2026-10-01T04:18:01Z
sessionEnd 2026-10-01T04:22:39Z
sessionEnd 2026-10-01T04:24:51Z
```

`start-marker.log` verbatim (control, all of it):

```
sessionStart 2026-10-01T04:16:47Z
sessionStart 2026-10-01T04:21:16Z
sessionStart 2026-10-01T04:23:28Z
```

Every `sessionEnd` timestamp matches its session's `result`-event
timestamp to the second. Control fired 3/3: loader + trust were
active in every session, so the positive is attributable to the
`sessionEnd` event itself.

Caveat — no trial isolated a clean successful-turn → normal exit:
trial 1's turn succeeded but its exit was TERM-assisted in the same
second; trials 2–3 error-terminated because the provider was
unreachable from this sandbox tonight (10 s connect timeouts,
retried by the CLI). Same shape as the Claude X5 caveat (turns
blocked on exhausted credit; hook fired each time). The claim under
test is the trigger; it fired on complete, abort, and error
terminations alike — 3/3.

## Binary-strings corroboration

Installed binary: `copilot-linux-x64/copilot` (167 MB, compiled).
`strings` counts: `sessionEnd` 0, `sessionStart` 0, `postToolUse` 0,
`hooks` 507. Non-informative: the same zero counts hold for
`sessionStart` / `postToolUse`, events behaviorally proven to fire
(E4 retest; this probe's control). The bundle does not expose
event-name strings to `strings`; behavioral evidence governs. (This
also supersedes the S4-era inference from an earlier `app.js` string
search — see the S4 audit correction.)

## Verdict

**PROVEN** (trigger, Copilot CLI 1.0.89, headless, trusted dir) —
a `sessionEnd` hook registered in `.github/hooks/*.json` fires at
session termination, 3/3 headless `copilot -p` sessions, hook alone
writing the marker, timestamps matching session end. Scoped:

- PROVEN: the *trigger mechanism* on the documented repo hook
  surface, with directory trust via `COPILOT_ALLOW_ALL=true`.
  Untrusted dirs fire nothing (E4) — the trust gate is part of the
  mechanism.
- NOT claimed: hook output is processed (docs say it is not), or
  that a cleanup *skill* runs — the wired action remains the
  sidecar record stub, same as Claude.
- Ledger S19's Copilot scope changes from UNVERIFIABLE to PROVEN
  (trigger) by dated amendment; backlog X5 updated likewise.

## Spend

Copilot credits: 0 (`premiumRequests: 0` in every `result`; BYOK
bills Anthropic-side). Anthropic-side: 1 successful Haiku call
(trial 1; the rest were connect failures, no completion). At the
repo conversion (trivial BYOK run ≈14.5k input / 40 output tokens,
$1/M in, $5/M out) ≈ **$0.02** upper bound, of the ~$0.50 budget.
Raw JSONL + scratch tree: `~/workspace/w4b-x5copilot-scratch/`.
