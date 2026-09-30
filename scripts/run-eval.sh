#!/usr/bin/env bash
# Packaged eval runner — one entry point.
#
#   ./scripts/run-eval.sh --task evals/tasks-packaged/<id> [--tool claude|copilot]
#                         [--arm base|agent|orient] [--agent <name>] [--orient <file>]
#                         [--source <git clone>] [--python <interpreter>]
#
# Runs the tool headlessly on the task's parent commit in a scratch tree,
# grades from disk with the real fix commit's tests, and writes
# evals/results/<date>-RUN-<id>-<tool>-<arm>.md with cost/turns + a verdict
# line. Exit codes: 0 PASS, 1 FAIL, 2 harness ERROR. See docs/feedback-loop.md.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/scripts/run_eval.py" --repo-root "$ROOT" "$@"
