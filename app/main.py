import uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_csrf_protect.exceptions import CsrfProtectError

from app.logger_setup import setup_logger
from app.routers import games_router, auth_router
from app.routers.auth import validate_csrf
from app.socket_managers.games_manager import GamesManager

games_manager: GamesManager = GamesManager()

app = FastAPI(title='wiki-me API', on_startup=[setup_logger])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change on production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.middleware('http')
# async def player_session(request: Request, call_next):
#     player_id = request.headers.get('Player-ID')  # TODO should I use my own header or cookies?
#
#     if not player_id:
#         return RedirectResponse('/auth/login', status_code=status.HTTP_401_UNAUTHORIZED)
#
#     if not Player.exists(player_id):
#         logger.warning(f'Player {player_id} does not exist', request=request)
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or does not exist")
#
#     response = await call_next(request)
#     response.headers['Player-ID'] = player_id
#     return response


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.message})


app.include_router(auth_router)
app.include_router(games_router, dependencies=[Depends(validate_csrf)])


@app.get('/')
def main(request: Request):
    return {'hello world'}


# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8080)

# TODO depends on cookie (he should first create
# @app.websocket("/ws/join/{game_id}")
# async def play(
#         websocket: WebSocket,
#         game_id: str,
#         session: Annotated[str | None, Cookie()] = None):
#     if session is None:
#         raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
#     player_id = websocket.state.player_id  # should have player_id in state after session_status middleware
#     player = Player(id=player_id, name='random name')
#     player_connection = PlayerConnection(websocket, player)
#     await player_connection.connect()
#     game_manager = games_manager.get_game_manager(game_id)
#     if not game_manager.has_reached_connections_limit():
#         game_manager.add_player(player_connection)
#         logger.success(f'player {player_id} has joined game {game_id}')
#         # TODO: should close connection?
#         # TODO: replace to HTTP request
#
#
# @app.websocket('/ws/game/')
# async def create_game(websocket: WebSocket, game: Game, player_id: uuid.UUID):
#     # TODO: should be http
#     player = PlayerConnection(websocket, player_id)
#     game_manager = GameRoom(game)
#     game_manager.add_player(player)
#     games_manager.add_game_manager(game_manager)
#     await game_manager.broadcast(f"new game created: {game_manager.game.url}")
