# Background job queue. The worker process calls run_pending()
# once per minute; jobs are plain callables.
_queue: list = []

def add_job(fn) -> None:
    _queue.append(fn)

def run_pending() -> None:
    jobs, _queue[:] = _queue[:], []
    for fn in jobs:
        fn()
