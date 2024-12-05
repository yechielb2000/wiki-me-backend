from fastapi import APIRouter

from app.models.game import Game

games_router = APIRouter(prefix="/games")


@games_router.get("/", tags=["games"])
async def games(game_id: str):
    game_room = Game.get(game_id)
    return game_room.model_dump()


@games_router.post("/", tags=["games"])
async def games(game: Game):
    game_model = Game.model_validate_json(game)
    game_model.create()
    return game_model.redis_key


@games_router.delete("/", tags=["games"])
async def games(game_id: str):
    """ Delete a game if you are the game admin. """
    pass
