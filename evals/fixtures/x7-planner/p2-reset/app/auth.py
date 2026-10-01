from app.users import get_user_by_email, hash_password

_sessions: dict[str, str] = {}

def login(email: str, password: str) -> str | None:
    user = get_user_by_email(email)
    if user is None or user.password_hash != hash_password(password):
        return None
    return _start_session(email)

def _start_session(email: str) -> str:
    token = f"sess-{email}"
    _sessions[token] = email
    return token

def logout(token: str) -> None:
    _sessions.pop(token, None)

def invalidate_sessions_for(email: str) -> None:
    for t in [t for t, e in _sessions.items() if e == email]:
        del _sessions[t]
