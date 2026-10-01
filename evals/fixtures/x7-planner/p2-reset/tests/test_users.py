from app.users import create_user, get_user_by_email

def test_create_user_hashes_password():
    create_user("x@y.z", "secret123")
    assert get_user_by_email("x@y.z").password_hash != "secret123"
