import hashlib
from dataclasses import dataclass

@dataclass
class User:
    email: str
    password_hash: str
    display_name: str = ""

_users: dict[str, User] = {}

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email: str, password: str, display_name: str = "") -> User:
    user = User(email, hash_password(password), display_name)
    _users[email] = user
    return user

def get_user_by_email(email: str) -> User | None:
    return _users.get(email)

def set_password(user: User, password: str) -> None:
    user.password_hash = hash_password(password)
