from datetime import datetime, timezone

# Convention: every stored timestamp is timezone-aware UTC.
# A 2026-07 incident came from mixing naive local times into
# published_at; always take the current time from now_utc().
def now_utc() -> datetime:
    return datetime.now(timezone.utc)
