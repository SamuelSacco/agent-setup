# X19 — version-guard probe — 2026-10-01

Question: does a standalone guard fail on each regression mode that
breaks the shared-AGENTS.md setup — old Claude Code, a bridgeless
CLAUDE.md, or the AGENTS.md marker no longer loading?

Branch: `feat/x19-version-guard` off master `ce0edbe`.

## Settled facts (not re-tested here)

- Native AGENTS.md load needs Claude Code >= v2.1.277.
- An annex-only CLAUDE.md (no `@AGENTS.md` bridge) suppresses the shared
  file (2/2 observed, `evals/results/2026-09-30-P2-claudemd-drop.md`).
- At head `ce0edbe` this tree already ships no CLAUDE.md and an earlier
  guard, `scripts/check-agents-md-load.sh` (ledger C4, final-shape proof
  `evals/results/2026-09-30-P2-claudemd-final-shape.md`). That guard
  waives the version floor when a bridged CLAUDE.md is present and
  checks only the root CLAUDE.md. X19 as specified requires failure on
  version < 2.1.277 unconditionally and on any bridgeless CLAUDE.md in
  the tree, so X19 lands as a new strict script,
  `scripts/check-version-guard.sh`; the existing guard and its
  run-eval preflight wiring are untouched.
- The keep-vs-delete CLAUDE.md ruling is Samuel's and remains PARKED.
  This run deletes nothing and changes no bridge.

## Pre-registered protocol (written before any test run)

Guard under test: `scripts/check-version-guard.sh`, exit 1 = invariant
failed, exit 2 = harness error, exit 0 = pass. Scratch copies live
under `~/workspace/x19-scratch/` (outside the clone); each is a minimal
tree containing copies of the repo's instruction files, mutated as
stated. The real CLI is never downgraded and the real tree is never
mutated.

Failure conditions and inductions:

1. **Old version.** PATH/CLAUDE_BIN shim: a fake `claude` executable
   whose `--version` prints `2.1.276 (Claude Code)`. Run the guard
   `--skip-live --root <clean scratch copy>` with
   `CLAUDE_BIN=<shim>`. Expected: exit 1, message names (1) and the
   floor. A second shim printing `2.1.277` exactly must PASS check (1)
   (boundary). Version-string robustness: shim outputs
   `v2.1.285`, bare `2.1.285`, and `claude version 2.1.285` must all
   parse and pass check (1) in static mode.
2. **Bridgeless CLAUDE.md.** Scratch copy + a `CLAUDE.md` containing
   annex text only (no bridge), plus a second bridgeless copy placed
   in a subdirectory of the same scratch tree. Run `--skip-live` with
   the real CLI. Expected: exit 1, message names (2) and the offending
   file. Positive control: scratch copy whose root `CLAUDE.md`
   contains the `@AGENTS.md` bridge line must pass (2) in static mode.
3. **Marker stops loading.** Two inductions:
   a. Marker removed: scratch copy with the marker sentence deleted
      from `AGENTS.md`. Run in static mode (`--skip-live`): expected
      exit 1 naming (3).
   b. Live probe: same marker-removed scratch copy, run `--live-only`
      (static bypassed) against the real CLI. Expected: exit 1, probe
      answers NOT LOADED (or without the marker tail). This is a paid
      probe (~$0.012).

Pass criteria (all required for PROVEN):

- Each induced failure above: guard exits 1 with a message naming the
  failed check.
- Clean tree: guard on the real repo root exits 0 in static mode, and
  exits 0 in full mode with the live probe reporting the marker loaded
  (at least one live run).
- Total metered spend <= $0.50 cap.

## Results

All runs 2026-10-01, real CLI `2.1.285 (Claude Code)` unless shimmed.
Scratch trees: `~/workspace/x19-scratch/` (outside the clone, deleted
after the run — outcomes transcribed below from the run output).

| Case | Command shape | Exit | Output (key line) |
|---|---|---|---|
| Clean tree, static | guard `--root <repo>` `--skip-live` | 0 | PASS (1) 2.1.285 >= 2.1.277; PASS (2) no CLAUDE.md; PASS (3) marker present |
| Clean tree, full (live) | guard `--root <repo>` | 0 | PASS (3) live probe 1/1: marker loaded (metered cost_usd=0.031075) |
| 1. Old version | shim prints `2.1.276`, `--skip-live` | 1 | FAIL (1) Claude Code 2.1.276 < 2.1.277 |
| 1b. Boundary | shim prints `2.1.277`, `--skip-live` | 0 | PASS (1) 2.1.277 >= floor; all static checks pass |
| 1c. Formats | shims print `v2.1.285` / `2.1.285` / `claude version 2.1.285` | 0 each | PASS (1) parsed as 2.1.285 in all three formats |
| 2. Bridgeless CLAUDE.md | annex-only root `CLAUDE.md`, `--skip-live` | 1 | FAIL (2) names the root CLAUDE.md |
| 2b. Nested only (supplementary, added to isolate recursion) | bridgeless `sub/CLAUDE.md` only, `--skip-live` | 1 | FAIL (2) names `sub/CLAUDE.md` — the tree search is recursive |
| 2c. Positive control | root `CLAUDE.md` with `@AGENTS.md` bridge, `--skip-live` | 0 | PASS (2) bridge detected; all static checks pass |
| 3a. Marker removed, static | marker sentence deleted, `--skip-live` | 1 | FAIL (3) marker sentence not found in AGENTS.md |
| 3b. Marker removed, live | same tree, `--live-only` | 1 | FAIL (3) probe answered `NOT LOADED` (run twice: first run's cost unreported — probe JSON was trap-deleted before capture; rerun after the guard was fixed to print cost on the FAIL path, metered cost_usd=0.0148674) |

Defect found and fixed during the run: the first static pass falsely
FAILed check (2) on trees with no CLAUDE.md (an empty `find` result fed
one empty line into the check loop). Fixed by collecting matches with
`find -print0` into an array; all cases above are from the fixed
script, re-run end to end.

## Verdict

- Condition (1) version floor: **PROVEN** — exit 1 at 2.1.276, exit 0
  at exactly 2.1.277, three version-string formats parsed.
- Condition (2) bridgeless CLAUDE.md: **PROVEN** — exit 1 for root and
  nested-only placements; bridged control passes.
- Condition (3) marker load: **PROVEN** — static marker check exit 1 on
  removal; live probe exit 1 (`NOT LOADED`) on the marker-removed
  tree; live probe exit 0 (marker loaded) on the clean tree.
- Clean tree, full mode: exit 0.

Scope: the guard checks the target tree only; a CLAUDE.md in a parent
directory of a consumer checkout remains outside its scope (W5
contamination caveat, unchanged).

## Spend

| Item | Cost |
|---|---|
| Static cases (all) | $0 |
| Live probe, clean tree ×1 | $0.031075 metered |
| Live probe, marker-removed ×1 (rerun, metered) | $0.0148674 |
| Live probe, marker-removed ×1 (first run, cost unreported) | ≈ $0.015 est. (same probe shape) |
| **Total** | **$0.0459424 metered; ≈ $0.061 including the unreported run** |

Cap $0.50 — not approached.
