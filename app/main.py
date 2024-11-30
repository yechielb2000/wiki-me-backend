from fastapi import FastAPI, WebSocket
from loguru import logger

from app.logger_setup import setup_logger
from app.models.game import Game
from app.socket_managers.game_room import GameRoom
from app.socket_managers.games_manager import GamesManager
from app.socket_managers.player import Player

app = FastAPI(title='wiki-me API', on_startup=[setup_logger])
games_manager: GamesManager = GamesManager()


# make token for session


@app.get("/games")
async def games(game_id: str):
    game_room = Game.load_from_redis(game_id)
    return game_room.model_dump()


@app.post("/games")
async def games(game: Game):
    game_model = Game.model_validate_json(game)
    game_model.save_to_redis()
    return game_model.redis_key


@app.delete("/games")
async def games(game_id: str):
    """ Delete a game if you are the game admin. """
    pass



# TODO depends on cookie (he should first create
@app.websocket("/ws/join/{game_id}")
async def join_game(websocket: WebSocket, game_id: str, player_id: str):
    player = Player(websocket, player_id)
    await player.connect()
    game_manager = games_manager.get_game_manager(game_id)
    if not game_manager.has_reached_connections_limit():
        game_manager.add_player(player)
        logger.success(f'player {player_id} has joined game {game_id}')
        # TODO: should close connection?
        # TODO: replace to HTTP request


@app.websocket('/ws/game/')
async def create_game(websocket: WebSocket, game: Game, player_id: str):
    player = Player(websocket, player_id)
    game_manager = GameRoom(game)
    game_manager.add_player(player)
    games_manager.add_game_manager(game_manager)
    await game_manager.broadcast(f"new game created: {game_manager.game.url}")


@app.websocket("/ws/play/{game_id}")
async def play_game(websocket: WebSocket, game_id: str, player_id: str):
    player = Player(websocket, player_id)
    await player.connect()
    game_manager = games_manager.get_game_manager(game_id)
    # game_manager.game_loop()
