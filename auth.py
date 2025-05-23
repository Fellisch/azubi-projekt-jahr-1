import bcrypt

from dataclasses import dataclass
from typing_extensions import Optional
from models import SessionLocal, User, Game

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
        print("❌ Username already exists.")
        return AuthAnswer(id=0,code=101)

    hashed_pw = hash_password(password)
    new_user = User(username=username, password=hashed_pw)
    session.add(new_user)
    session.commit()
    print("✅ User registered.")
    return AuthAnswer(id=new_user.id,code=None)


def login_user(username: str, password: str) -> AuthAnswer:
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print("❌ User not found.")
        return AuthAnswer(id=0, code=102)

    if verify_password(password, user.password):
        print("✅ Login successful!")
        return AuthAnswer(id=user.id, code=102)
    else:
        print("❌ Incorrect password.")
        return AuthAnswer(id=0, code=103)

def updateUserData(id: int, username: str, password: str):
    session = SessionLocal()
    user = session.query(User).filter(User.id==id).first()
    if user:
        user.username = username
        user.password = hash_password(password)
        session.commit()