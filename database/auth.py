import bcrypt

from dataclasses import dataclass
from typing_extensions import Optional
from .models import SessionLocal, User, Game
from sqlalchemy.exc import IntegrityError

class AuthAnswer:
    id: int
    code: Optional[int]

    def __init__(self,id: int, code: Optional[int]):
        self.id = id
        self.code = code

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def register_user(username: str, password: str) -> AuthAnswer:
    session = SessionLocal()
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        print("DEBUG: Username already exists in register_user.")
        session.close()
        return AuthAnswer(id=0,code=101)

    hashed_pw = hash_password(password)
    new_user = User(username=username, password=hashed_pw)
    session.add(new_user)
    session.commit()
    user_id = new_user.id
    session.close()
    print(f"DEBUG: User {username} registered successfully with ID: {user_id}.")
    return AuthAnswer(id=user_id,code=None)


def login_user(username: str, password: str) -> AuthAnswer:
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print("DEBUG: User not found in login_user.")
        session.close()
        return AuthAnswer(id=0, code=102)

    if verify_password(password, user.password):
        print(f"DEBUG: Login successful for user {username}.")
        session.close()
        return AuthAnswer(id=user.id, code=None)
    else:
        print("DEBUG: Incorrect password in login_user.")
        session.close()
        return AuthAnswer(id=0, code=103)

def updateUserData(id: int, username: str, password: str):
    session = SessionLocal()
    user = session.query(User).filter(User.id==id).first()
    if user:
        user.username = username
        user.password = hash_password(password)
        session.commit()
    session.close()

# Placeholder for login (not fully implemented here yet)
# def verify_user(username: str, password_plain: str) -> User | None:
#     session = SessionLocal()
#     user = session.query(User).filter(User.username == username).first()
#     session.close()
#     if user and bcrypt.checkpw(password_plain.encode('utf-8'), user.password.encode('utf-8')):
#         return user
#     return None