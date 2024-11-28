from fastapi import FastAPI, WebSocket
from loguru import logger

from app.logger_setup import setup_logger
from app.models.game import Game
from app.socket.game_manager import GameManager
from app.socket.games_manager import GamesManager
from app.socket.player import Player

setup_logger()
app = FastAPI(title='wiki-me API')
games_manager: GamesManager = GamesManager()  # This should be generated for new room create.


@app.get("/{game_id}")
async def games(game_id: str):
    return games_manager.get_game_manager(game_id)


@app.post("/")
async def games():
    return


@app.delete("/")
async def games():
    return


@app.get("/")
async def games():
    return


# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await socket.connect(websocket)
#     if websocket in socket.active_connections:
#         await socket.broadcast(f"{socket.active_connections}")
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await socket.send_personal_message(f"You wrote: {data}", websocket)
#             await socket.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         socket.disconnect(websocket)
#         await socket.broadcast(f"Client #{client_id} left the chat")

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


# TODO: join a game
@app.post('/game/{game_id}')
async def join_game_http_v(game_id: str, player_id: str):
    pass


@app.websocket('/ws/game/')
async def create_game(websocket: WebSocket, game: Game, player_id: str):
    player = Player(websocket, player_id)
    game_manager = GameManager(game)
    game_manager.add_player(player)
    games_manager.add_game_manager(game_manager)
    await game_manager.broadcast(f"new game created: {game_manager.game.url}")


@app.websocket("/ws/play/{game_id}")
async def play_game(websocket: WebSocket, game_id: str, player_id: str):
    player = Player(websocket, player_id)
    await player.connect()
    game_manager = games_manager.get_game_manager(game_id)
    # game_manager.game_loop()
