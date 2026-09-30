---
session_id: 2026-09-30-1115-helm-orientation-second-codebase
tool: helm
model: claude-haiku-4-5-20251001 (eval runs)
started: 2026-09-30 11:15 EDT
status: in-progress
intent: Replicate the Claim B orientation A/B on a second codebase (Rich) under identical discipline.
---

# Session: Orientation replication, second codebase (Rich)

## Intent
Samuel authorized (2026-09-30 11:11 ET) spending the remaining Phase 2
budget to test the orientation claim on a second codebase — the claim
is the talk's headline and rested on NetworkX alone (n=8). One variable
changes: the codebase. Same model, arms, prereg discipline.

## Starting state
- Branch `phase-2` at 4489b04, clean. V1 tag/master untouched.
- Claim B: PROVEN on NetworkX (combined n=8: base 6/8, orientation
  8/8; ledger S12). Claim A not under test.
- Infra reused: W3/replication runner pattern
  (`~/workspace/p2/portverify/repl_runner.py`).

## Turn log

### 11:15 — Orientation and design
- **Intended:** absorb W3 + replication method exactly before changing anything.
- **Tried:** read P2-realcode-ab.md (incl. replication section), prereg file, repl_runner.py, ledger S12, repo AGENTS.md.
- **Happened:** method pinned: git-archive isolation, overlay grading, frozen orientation text, Claim B rule. This session varies only the codebase.

### 11:20 — Codebase setup (Rich)
- **Intended:** mid-size Python project, different domain, tests run in sandbox.
- **Tried:** cloned Textualize/rich @ 9d8f9a37 into `~/workspace/p2/secondcode/.infra/rich-src`; built venv (Python 3.12.3, pytest 9.1.1, Pygments 2.21.0, markdown-it-py 4.2.0, attrs 26.1.0).
- **Happened:** clone clean; ~26.6k LOC library, ~11.2k LOC tests.

### 11:25 — Mining and oracle validation
- **Intended:** 4 tasks from real fix commits, W3 filters, oracle-validated before any run.
- **Tried:** scanned last 800 non-merge commits (18 candidates). Validated 7 finalists in exported trees (grading tests at commit vs at parent + test overlay).
- **Happened:** selected U1 pretty `6055e2d8e`, U2 console `39ee57dfe`, U3 cells `13f87a400`, U4 table `1c5e03eb3` — all pass at commit, fail at parent. Dropped: text.py `f2ee29531` (grading test hangs at parent — infinite loop), segment `4f40703e4` (test fails at its own fix commit in this env, inverted), markdown `7ef2d05ca` (own test fails at fix commit in this env, Pygments-sensitive). Drops recorded in the prereg section.

### 11:35 — Pre-registration committed before runs
- **Intended:** prereg discipline identical to W3: section appended to the results file and committed before any agent run.
- **Tried:** appended "Second codebase (Rich)" section to `evals/results/2026-09-30-P2-realcode-ab.md` (tasks, validation, arms, Claim B rule, combined-verdict rule, $6 cap); wrote frozen Rich orientation text + 4 prompts + runner under `~/workspace/p2/secondcode/`.
- **Happened:** pending commit at time of writing; runs start only after the push lands.

## Learned
- Rich's snapshot-style rendering tests can be environment-sensitive at their own fix commits (Unicode data, Pygments versions) — oracle validation must run in the grading environment, not be assumed from the commit's CI.

## Outcome
in-progress — runs and verdicts to follow in this record.
