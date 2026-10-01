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

## Results

(appended after the runs; prereg above is the committed pre-run text)
