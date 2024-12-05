from fastapi import APIRouter, WebSocket
from loguru import logger

from app.models.game import Game
from app.models.player import Player
from app.socket_managers.games_manager import GamesManager
from app.socket_managers.player_connection import PlayerConnection

games_manager: GamesManager = GamesManager()
games_router = APIRouter(prefix="/games")


@games_router.get("/", tags=["games"], response_model=Game)
async def games(game_id: str):
    game = await Game.get(game_id)
    return game


@games_router.post("/", tags=["games"], response_model=Game)
async def games(game: Game):
    await game.create()
    return game


@games_router.delete("/", tags=["games"])
async def games(game_id: str):
    """ Delete a game if you are the game admin. """
    pass


@games_router.websocket("/ws")
async def play(websocket: WebSocket, game_id: str, player_id: str):
    player_id = player_id or websocket.state.player_id  # should have player_id in state after session_status middleware
    player = await Player.get(player_id)
    player_connection = PlayerConnection(websocket, player)
    await player_connection.connect()
    game_manager = games_manager.get_game_manager(game_id)
    if game_manager.has_reached_connections_limit():
        logger.warning(f'Game has reached connections limit ({game_manager.game.max_connections})')
        await player_connection.disconnect()
        return
    game_manager.add_player(player_connection)
    logger.success(f'player {player_id} has joined game {game_id}')
