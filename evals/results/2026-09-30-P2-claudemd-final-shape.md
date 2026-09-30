# W3 — CLAUDE.md final-shape proof — 2026-09-30

Question: with the guard in place, can this repo ship NO `CLAUDE.md` —
one shared `AGENTS.md`, loaded natively by both tools?

Branch: `change/no-claudemd` (from `phase-2` @ 3556e46). Follows W5
(`2026-09-30-P2-claudemd-drop.md`, verdict PARTIAL, keep-the-bridge)
under Samuel's 2026-09-30 14:24 ET directive: execute the drop with
proof and a guard, or refute it. Ledger claim C4 amended.

## What changed

- `CLAUDE.md` deleted (its only content: the `@AGENTS.md` bridge, a
  `/context` tip whose referent is now `AGENTS.md`, and a pointer to
  `docs/tips-claude.md` that `AGENTS.md` already makes).
- Guard: `scripts/check-agents-md-load.sh`. Exit 1 if any invariant
  breaks:
  - (a) `CLAUDE.md` absent and installed Claude Code < 2.1.277 (the
    native-`AGENTS.md` floor).
  - (b) a `CLAUDE.md` exists without the `@AGENTS.md` bridge line —
    the suppression trap (W5 arm C).
  - (c) a live Claude probe in a consumer project built from this
    tree's instruction files fails to load the shared marker (the
    `AGENTS.md` §1 sentence ending "makes the wiki compound").
  Exit 2 = harness error (no binary/helper, unparseable output).
- Wiring: `scripts/run_eval.py` runs the guard in `--static` mode as a
  preflight before any eval spends money (`--skip-preflight` bypasses).
  Full live mode is one command: `scripts/check-agents-md-load.sh
  --runs 2`.

## Versions (verbatim)

```
$ claude --version
2.1.285 (Claude Code)
$ copilot --version
GitHub Copilot CLI 1.0.89.
```

## Final-shape proof (no CLAUDE.md anywhere in the tree)

Consumer project = this branch's `AGENTS.md` alone in a clean /tmp
tree, fresh HOME per run, `.claude/settings.json` apiKeyHelper auth,
model `claude-haiku-4-5-20251001`. Probe asks for the marker sentence
verbatim; "NOT LOADED" if absent.

| Probe | Result | Evidence |
|---|---|---|
| Guard, `--runs 2` (Claude) | 2/2 marker loaded | guard PASS lines (a), (b), (c)×2; debug log confirms loader |
| Claude evidence run 1 | marker quoted | result: `Do not skip orientation to "save time." Orientation is what makes the wiki compound.` — cost $0.01202115; debug log: `no CLAUDE.md found; AGENTS.md loaded: /tmp/w3proof/final/project/AGENTS.md` |
| Claude evidence run 2 | marker quoted | result: `Orientation is what makes the wiki compound.` — cost $0.01385615; same loader line |
| Copilot (BYOK, same key/model) | marker quoted | same sentence returned; footer 15.8k in / 179 out (≈$0.0167 upper-bound converted) |

## Negative controls (the guard must catch the trap)

Stub tree = final shape + an annex-only `CLAUDE.md` (no bridge):

| Control | Outcome |
|---|---|
| Guard, default mode | **exit 1** — FAIL (b): "CLAUDE.md exists WITHOUT the @AGENTS.md bridge" |
| Guard, `--skip-static` (live probe only) | **exit 1** — FAIL (c): probe answered `NOT LOADED`; suppression reproduced live in this tree shape |
| Guard, `--static`, tree with the old bridged `CLAUDE.md` restored | exit 0 — PASS (b): bridge detected |
| run-eval preflight vs stub tree | run-eval dies **exit 2** before any spend: "preflight: AGENTS.md-load guard failed" |
| run-eval preflight vs this branch | PASS lines (a)+(b), eval proceeds — full nx-t2 run graded end-to-end: **PASS (1/1 nodes), 9 turns, $0.108047 metered, 248 s** |

## Verdict

**PROVEN** for the final shape on the tested surfaces (Claude Code
2.1.285 direct API; Copilot CLI 1.0.89 BYOK): with `CLAUDE.md` deleted,
the shared `AGENTS.md` loads natively in both tools, and the guard
catches every regression mode W5 identified — version floor, bridgeless
`CLAUDE.md` (statically and live), marker loss. Accepted losses,
unchanged from W5: the annex content (relocated — `/context` now
checks `AGENTS.md`; tool niceties already in `docs/tips-claude.md`)
and `InstructionsLoaded` hook firing for the main instruction file.
The all-or-nothing caveat stands: the guard protects THIS tree; a
`CLAUDE.md` introduced in a PARENT directory of a consumer checkout
is outside its scope (W5 contamination finding).

## Cost log

| Item | Cost |
|---|---|
| Guard live probes ×2 (final shape) | ≈ $0.026 (metered class, same probe shape as evidence runs) |
| Claude evidence runs ×2 | $0.01202115 + $0.01385615 = $0.02587730 |
| Copilot probe ×1 | ≈ $0.0167 (upper-bound conversion) |
| Negative-control live probe ×1 | ≈ $0.012 (metered class) |
| Wiring eval run (nx-t2, claude/base) | $0.108047 (the PASS run above) |
| Duplicate wiring attempts ×2 | $0.245 + $0.161 — the harness backgrounded two earlier launches of the same wiring test, which kept running concurrently and completed their tool stages; disclosed, not hidden. (First attempt also used a stale EVAL_PYTHON path; its grading never landed.) |
| **Total** | **≈ $0.59** |

Raw evidence (ephemeral, /tmp): `/tmp/w3proof/final/` (project, probe
JSON, debug logs, copilot output), `/tmp/w3proof/neg/`,
`/tmp/w3proof/bridged/`, `/tmp/w3proof/wiring-run.log`.
