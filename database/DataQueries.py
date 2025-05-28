from models import SessionLocal, User, Game

def increaseWins(id: int, gamemode: int, difficulty: int):
    session = SessionLocal()
    game = session.query(Game).filter(Game.userId==id,Game.gamemode==gamemode,Game.difficulty==difficulty).first()
    if game:
        game.wins += 1
        session.commit()

def increaseLosses(id: int, gamemode: int, difficulty: int):
    session = SessionLocal()
    game = session.query(Game).filter(Game.userId==id,Game.gamemode==gamemode,Game.difficulty==difficulty).first()
    game.losses += 1
    session.commit()

def getPlayersWithMostWins(gamemode: int, difficulty: int) -> list:
    session = SessionLocal()
    games = (session.query
        (User.username,
        Game.wins,
        Game.losses)
        .join(Game, Game.userId == User.id)
        .filter(Game.gamemode == gamemode, Game.difficulty == difficulty)
        #.group_by(Game.userId)
        .all())
    return games