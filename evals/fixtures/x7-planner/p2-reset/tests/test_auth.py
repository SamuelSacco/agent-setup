from app.auth import login, logout
from app.users import create_user

def test_login_roundtrip():
    create_user("a@b.c", "pw123456")
    token = login("a@b.c", "pw123456")
    assert token
    logout(token)
