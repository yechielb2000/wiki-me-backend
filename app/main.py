from fastapi import FastAPI, WebSocket

from app.socket.games_manager import GamesManager

app = FastAPI()
socket: GamesManager = GamesManager()  # This should be generated for new room create.


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


@app.websocket_route(path="/ws/{room_id}/{client_id}")
async def websocket_client(webscoket: WebSocket, room_id: str, client_id: str):
    pass
