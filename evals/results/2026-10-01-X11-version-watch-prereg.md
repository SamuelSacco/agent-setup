# X11 version-watch — preregistration (2026-10-01, Wave 4-B)

Item: Q9 / X11. Ledger: S4 (Copilot arm). Backlog: X11.
Hard metered cap: $0.75. Stop at cap, report honestly.

## Dead-state inspection (coordinator, recorded here, not redone)

- Clone `~/workspace/w2c-x11-watch`, branch `wave2c/x11-version-watch`:
  ZERO unique commits — no usable X11 work.
- Branches `wave2c/x9-e6-claude-arm` and `wave2c/x9-e6-copilot-arm`
  are X9 preregs, not X11.
- This run starts clean on branch `lab/x11-version-watch` off current
  `origin/master` (210df66 at branch creation).

## Prior verdict under watch

X11 status (backlog): REFUTED on installed CLI v1.0.89 (0/5 on the E4
Copilot arm). Audit correction on file (E4 addendum, ledger S4): the
"binary contains no hook loader" mechanism is retracted — hooks fire
in trusted dirs; `postToolUseFailure` does not fire for shell failures
(shell tool reports `resultType: success` even on exit 127). Copilot
leg = PARTIAL-with-mechanism. Cheapest decisive test, unchanged: on
the next Copilot CLI release, re-run the E4 Copilot arm unchanged.

## Mixed evidence to reconcile (before any re-run)

- `copilot --version` prints 1.0.90 tonight; Q15 runs executed under
  CLI 1.0.90.
- X13-era runtime logs reported 1.0.89.
- Ground truth required, with evidence not assertion:
  1. Binary path of the installed CLI.
  2. `copilot --version` output.
  3. Version the runtime reports inside an actual session
     (`session.start` event `copilotVersion` in
     `~/.copilot/session-state/<id>/events.jsonl`, or process log).
  4. Installed package metadata (`package.json` version fields for
     `@github/copilot` and the platform package).
  5. Whether the installed build is a release newer than the
     X11-tested 1.0.89. Reconcile any `--version` vs package-metadata
     vs runtime-log discrepancy by naming which artifact carries
     which version string and which one governs a session.

## Protocol — E4 Copilot arm, UNCHANGED (only if newer release)

Run only if ground truth shows the installed CLI is a release newer
than 1.0.89. If not newer: no eval run, verdict stands, watch
continues.

- Task: `evals/tasks/E4-failure-capture.md`, Copilot arm, identical
  induced failures (concrete forms as recorded in
  `evals/results/2026-09-30-E4.md`):
  1. `python --version` (python3-only box, exit 127)
  2. `cat` of a nonexistent file (exit 1)
  3. Failing test run: `python3 -m unittest` of a missing module (exit 1)
  4. Invalid JSON: `python3 -m json.tool` on invalid JSON (exit 1)
  5. Command with exit code 2 (`exit 2`)
- Wiring: shipped adapter output only — `.github/hooks/failure-capture.json`
  as emitted by `scripts/install.sh` (`postToolUseFailure` →
  `./scripts/sidecar.sh record-failure`), plus `scripts/sidecar.sh`,
  in a scratch dir under `~/workspace`. No hook edits, no fallback
  wiring, no transcript mining. That is the "unchanged" condition.
- Trust: directory trust via `COPILOT_ALLOW_ALL=true` plus
  `--allow-all-tools --allow-all-paths` (allow-all in scratch only,
  standing authorization). The original 0/5 ran untrusted; the E4
  addendum established trust as part of the mechanism, and X5 ran
  trusted on 1.0.89. One prompt, one session, instructing the agent to
  run the 5 commands in order and continue after each failure.
- Model/provider: BYOK Anthropic, Haiku 4.5
  (`claude-haiku-4-5-20251001`), key via the vault helper, never
  printed or committed — same as all prior Copilot arms.
- PASS bar (pre-registered in E4, unchanged): ≥4/5 induced failures
  produce a parseable JSONL event in `wiki/telemetry/events.jsonl`
  (scratch-local store written by the shipped sidecar) with
  timestamp (`ts`) + `kind`. Count events, parse every line.
- Cost: read the raw footer of the run output. CLI 1.0.90 emits
  lowercase cost footers; converted cost at the repo convention
  ($1/M input, $5/M output, cached at full rate = upper bound) if
  only token totals are shown. Verify any figure against the raw
  footer text before reporting.

## Decision rules (fixed in advance)

- Newer release + ≥4/5 events: X11 verdict changes — failure capture
  on Copilot PROVEN on the new release; S4 Copilot arm updated.
- Newer release + 1–3/5 events: PARTIAL on the new release; per-failure
  table governs.
- Newer release + 0/5 events: REFUTED stands, now on the new release;
  mechanism note updated (shell-failure payload shape re-checked in
  the session transcript if present).
- No newer release (installed = 1.0.89): no run; verdict stands
  REFUTED/PARTIAL-with-mechanism as recorded; watch continues.

## Artifacts

- This prereg: committed in-branch before any eval run.
- Verdict: `evals/results/2026-10-01-X11-version-watch.md` with
  per-failure results, ground-truth table, raw footer, spend.
- Updates in-branch: `docs/claims-ledger.md` (S4 row, Copilot arm),
  `docs/experiments-backlog.md` (X11).
- `./scripts/install.sh` in this clone must exit 0 before finishing.
