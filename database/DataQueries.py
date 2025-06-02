from .models import SessionLocal, User, Game

def increaseWins(id: int, gamemode: int, difficulty: int):
    session = SessionLocal()
    game = session.query(Game).filter(Game.userId==id,Game.gamemode==gamemode,Game.difficulty==difficulty).first()
    if game:
        game.wins += 1
    else:
        # Create a new game record if it doesn't exist
        new_game = Game(userId=id, gamemode=gamemode, difficulty=difficulty, wins=1, losses=0)
        session.add(new_game)
    session.commit()
    session.close() # Close the session

def increaseLosses(id: int, gamemode: int, difficulty: int):
    session = SessionLocal()
    game = session.query(Game).filter(Game.userId==id,Game.gamemode==gamemode,Game.difficulty==difficulty).first()
    if game:
        game.losses += 1
    else:
        # Create a new game record if it doesn't exist
        new_game = Game(userId=id, gamemode=gamemode, difficulty=difficulty, wins=0, losses=1)
        session.add(new_game)
    session.commit()
    session.close() # Close the session

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