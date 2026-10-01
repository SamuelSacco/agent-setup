# Passkeep
User-account service. Layout: `app/users.py` user records,
`app/auth.py` login/sessions, `app/security.py` credential helpers,
`app/emailer.py` outbound mail, `app/oauth.py` third-party sign-in,
`app/db.py` storage, `app/config.py` settings. Tests in `tests/`.
Run: `python -m pytest tests/ -q`.
