# Periodic jobs. Jobs are registered at startup and run by the
# external cron driver calling run_daily_jobs() once a day.
JOBS: list = []

def register_job(name: str, fn) -> None:
    JOBS.append((name, fn))

def run_daily_jobs() -> None:
    for _name, fn in JOBS:
        fn()
