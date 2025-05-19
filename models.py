import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

engine = create_engine(
    os.getenv('DATABASE_URL'),
    echo=True
)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String, nullable=False)


Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
