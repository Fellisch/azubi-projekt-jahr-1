import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

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

    games = relationship("Game",back_populates="user")

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('users.id'))
    difficulty = Column(Integer,nullable=False)
    wins = Column(Integer,nullable=False)
    losses = Column(Integer,nullable=False)
    gamemode = Column(Integer,nullable=False)

    user = relationship("User",back_populates="games")

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
