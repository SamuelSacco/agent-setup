# Third-party OAuth sign-in (Google). Separate flow from password
# login in app/auth.py; OAuth users have no local password.
def oauth_callback(provider: str, code: str) -> str:
    return f"oauth-session-{provider}"
