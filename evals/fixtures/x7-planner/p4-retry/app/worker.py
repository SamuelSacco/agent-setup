import time

# Background worker: the ONLY place long-running or repeated work
# runs. app/api.py handlers must return fast and never loop/retry
# inline (worker policy, 2026-08 review).
BACKOFF_SECONDS = [60, 300, 1800]  # per-attempt delays for retries

_queue: list = []

def enqueue(fn) -> None:
    _queue.append(fn)

def process_queue() -> None:
    while _queue:
        fn = _queue.pop(0)
        fn()
