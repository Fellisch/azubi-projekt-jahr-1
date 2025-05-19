import bcrypt
from models import SessionLocal, User


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def register_user(username: str, password: str):
    session = SessionLocal()
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        print("❌ Username already exists.")
        return

    hashed_pw = hash_password(password)
    new_user = User(username=username, password=hashed_pw)
    session.add(new_user)
    session.commit()
    print("✅ User registered.")


def login_user(username: str, password: str):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print("❌ User not found.")
        return

    if verify_password(password, user.password):
        print("✅ Login successful!")
    else:
        print("❌ Incorrect password.")
