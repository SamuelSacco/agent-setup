---
session_id: 2026-10-01-0016-helm-x19-version-guard
tool: claude-code
model: unknown
started: 2026-10-01 00:16 EDT
status: complete
intent: Build the X19 version guard (strict floor + bridge + marker) and prove each failure condition by induced failure in scratch copies.
---

# Session: X19 version guard

## Intent
Backlog X19: build the guard that is buildable regardless of Samuel's
parked keep-vs-delete CLAUDE.md ruling. Do not delete CLAUDE.md; do not
change the bridge.

## Starting state
Branch `feat/x19-version-guard` off master `ce0edbe`. At head the tree
already ships no CLAUDE.md and a C4 guard
(`scripts/check-agents-md-load.sh`) that waives the version floor when
a bridged CLAUDE.md is present and checks only the root file — the
X19 spec is stricter, so X19 lands as a new script.

## Turn log

### 00:16 — Pre-registration
- **Intended:** Fix the test protocol before any run.
- **Tried:** Wrote `scripts/check-version-guard.sh`; wrote the
  pre-registered protocol into
  `evals/results/2026-10-01-X19-version-guard.md`.
- **Happened:** Protocol on disk before the first test invocation.

### 00:16 — Static inductions
- **Intended:** Exit 1 on old version (shim), bridgeless CLAUDE.md
  (root and nested), marker removed; exit 0 on clean/bridged/boundary.
- **Tried:** Scratch trees under `~/workspace/x19-scratch/`; version
  via `CLAUDE_BIN` shim (real CLI never downgraded).
- **Happened:** First pass exposed a guard bug — empty `find` result
  fed one empty line into the CLAUDE.md loop, false FAIL on clean
  trees. Fixed (`find -print0` into an array), full suite re-run:
  every case at its pre-registered exit code.

### 00:16 — Live probes
- **Intended:** Marker loads on the clean tree; NOT LOADED on the
  marker-removed tree.
- **Tried:** Full mode on the repo root; `--live-only` on the
  marker-removed scratch tree (twice — the first run's metered cost
  was trap-deleted before capture; the guard now prints cost on the
  FAIL path too).
- **Happened:** Clean exit 0, marker loaded, $0.031075. Marker-removed
  exit 1, probe `NOT LOADED`, $0.0148674 (rerun).

## Learned
- The C4 guard and the X19 spec differ on the version floor: C4 waives
  it with a bridged CLAUDE.md; X19 requires unconditional failure.
  Both scripts now coexist; X19 does not touch the run-eval preflight.

## Outcome
Complete. Evidence:
`evals/results/2026-10-01-X19-version-guard.md`. Spend $0.0459424
metered (≈$0.061 incl. one unreported probe run) of $0.50 cap.
CLAUDE.md ruling remains parked for Samuel.
