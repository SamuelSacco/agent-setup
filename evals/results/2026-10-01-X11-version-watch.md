# X11 version-watch — E4 Copilot arm re-run on CLI 1.0.90 (2026-10-01)

Item: Q9 / X11. Ledger: S4 (Copilot arm). Prereg:
`evals/results/2026-10-01-X11-version-watch-prereg.md` (committed
before any run). Branch: `lab/x11-version-watch`.

## Verdict

**REFUTED stands, now on Copilot CLI 1.0.90.** The installed CLI is
a release newer than the X11-tested 1.0.89, the E4 Copilot arm was
re-run unchanged, and it scored **0/5** — identical outcome and
identical mechanism to 1.0.89. PASS bar was ≥4/5. The 1.0.90 release
does not change the X11 verdict; the watch continues to the next
release.

## Ground truth — version reconciliation

| Artifact | Version | Evidence |
|---|---|---|
| `copilot --version` | **1.0.90** | "GitHub Copilot CLI 1.0.90." |
| Runtime, this run's session | **1.0.90** | `session.start` event: `"copilotVersion":"1.0.90"`, session `074886be-b764-4e29-8898-599a10d56888`, start 2026-10-01T05:18:55Z |
| Runtime, process log | **1.0.90** | "No update needed, current version is 1.0.90, fetched latest release is v1.0.90" (2026-10-01T05:18:53Z, this run; also 05:05:01Z) |
| npm wrapper metadata | 1.0.89 (stale) | `~/workspace/tools/lib/node_modules/@github/copilot/package.json` and `.../@github/copilot-linux-x64/package.json` both read `"version": "1.0.89"` |
| Native binary in npm tree | 1.0.89 (launcher) | `.../copilot-linux-x64/copilot`, 174,066,496 B, mtime 2026-09-30 04:20 UTC; literal strings: `1.0.89` ×10, `1.0.90` ×0 |
| Auto-update cache package | **1.0.90** | `~/.cache/copilot/pkg/linux-x64/1.0.90/package.json` reads `"version": "1.0.90"`; cache holds 1.0.83 / 1.0.89 / 1.0.90 side by side |

Mechanism of the discrepancy: the npm-installed 1.0.89 binary is a
launcher that checks the latest release at startup and executes the
newest package from `~/.cache/copilot/pkg/linux-x64/<version>/`.
The npm `package.json` fields never move; the running build does.

- X13-era logs reported 1.0.89 because then it was current: process
  logs 2026-09-30T18:39Z read "current version is 1.0.89, fetched
  latest release is v1.0.89".
- Session-state boundary on disk: last `copilotVersion: 1.0.89`
  session starts 2026-10-01T04:13:09Z; first `1.0.90` session starts
  2026-10-01T04:19:55Z. The 1.0.89 → 1.0.90 transition happened in
  that window tonight. Counts: 44 sessions at 1.0.89, 13 at 1.0.90.
- Conclusion: 1.0.90 is a real, newer release and it is the build
  that ran tonight (Q15, X13-isolation, and this run). The
  re-run condition in the prereg fired.

## E4 Copilot arm re-run (unchanged)

- Scratch: `~/workspace/w4b-x11-scratch/` (git-initialised), shipped
  wiring only: `.github/hooks/failure-capture.json` exactly as
  emitted by `install.sh` (`postToolUseFailure` →
  `./scripts/sidecar.sh record-failure`) + `scripts/sidecar.sh`
  copied from this repo. No hook edits, no fallback, no transcript
  mining.
- Trust: `COPILOT_ALLOW_ALL=true` + `--allow-all-tools
  --allow-all-paths`; isolated `COPILOT_HOME` in scratch (no user
  MCP servers). BYOK Anthropic, `claude-haiku-4-5-20251001`, key via
  vault helper (never printed/committed).
- Hook loader was active: this run's process log records "Loading
  repo hooks in prompt mode (folder is trusted or opt-in set)".
  The 0/5 is not a trust/loader failure.
- One headless session, prompt instructing the 5 induced failures in
  order, continue after each. All 5 executed.

| # | Induced failure | Exit | Sidecar event |
|---|---|---|---|
| 1 | `python --version` | 127 | none |
| 2 | `cat does-not-exist.txt` | 1 | none |
| 3 | `python3 -m unittest test_missing_module_x11` | 1 | none |
| 4 | `python3 -m json.tool bad.json` (invalid JSON) | 1 | none |
| 5 | `exit 2` | 2 | none |

Exit codes match the original E4 record exactly (127, 1, 1, 1, 2).
Score: **0/5**. `wiki/telemetry/events.jsonl` was never created in
the scratch store — the sidecar (which creates the file on any
invocation) was never invoked.

## Mechanism (re-checked on 1.0.90, unchanged from 1.0.89)

All 5 `tool.execution_complete` events in this session's transcript
carry `success: true`. The failure exists only in the result text
(`<shellId: N completed with exit code 127>` etc.). At the tool
layer a failed shell command is a success, so `postToolUseFailure`
has nothing to fire on — the same payload shape documented in the
E4 addendum for 1.0.89. The identified fallback (a `postToolUse`
hook parsing the exit-code text) remains unbuilt; this re-run did
not test it — unchanged arm only.

## Spend

Raw footer (verbatim, BYOK — no dollar line):
`Tokens ↑ 92.8k (76.5k cached, 16.3k written) • ↓ 1.1k (479 reasoning)`.
Exact usage from the session shutdown event: input 92,827, output
1,114 (6 requests). Converted at the repo convention ($1/M in,
$5/M out, cached at full rate = upper bound):
$0.092827 + $0.00557 = **$0.0984 of the $0.75 cap**.
Raw output: `evals/results/2026-10-01-X11-version-watch-run-output.txt`.
Wall: 64 s (footer `Duration 1m 4s`).

## Ledger / backlog effect

- S4 Copilot arm: REFUTED extended to CLI 1.0.90 (0/5, same
  mechanism). Overall S4 stays PARTIAL (Claude arm PROVEN 5/5).
- X11: verdict stands; cheapest decisive test unchanged — re-run on
  the next Copilot CLI release after 1.0.90.
