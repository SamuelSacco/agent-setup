#!/usr/bin/env bash
# Weekly verify: run all drift checks against the real repo + HOME.
# Stable path for a weekly cron. Propagates drift_check.py's exit code.
set -uo pipefail
exec python3 "$(dirname "$0")/drift_check.py" all
