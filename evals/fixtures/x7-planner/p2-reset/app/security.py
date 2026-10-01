import hashlib

# Convention (security review, 2026-08): bearer tokens are stored
# ONLY as SHA-256 hashes. A raw token must never be persisted, so a
# storage leak does not hand out usable tokens. hash_token() is the
# one helper for this; sessions follow the same rule in auth.py.
def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode()).hexdigest()

SESSION_TTL_MINUTES = 60
