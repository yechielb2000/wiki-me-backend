import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.socket.rooms_manager import RoomsManager
from src.socket.room import Room
from src.socket.player import Player

app = FastAPI()
rooms_manager: RoomsManager = RoomsManager()


@app.websocket("/ws/{player_name}")
async def join_room(websocket: Player, player_name: str, room_id: str):
    player: Player = websocket.set_name(player_name)
    room: Room = rooms_manager.get_room_if_exists(room_id)
    if not room:
        player.close(reason=f"Room id ({room_id}) does not exists.")
        return
    if not room.get_player_if_exists(player_name):
        player.close(reason="Name is already taken.")
        return
    try:
        await room.connect(player)
        if player in room.active_players:
            await room.broadcast(json.dumps(room.active_players))
        while True:
            # once the admin clicked `play` they get `start point` and `end point`.
            # then, we wait to see who is the first one to send he right link.
            # maybe its a good idea to set a timer...
            data = await player.receive_text()
            await room.broadcast(f"{player_name} has won the game!")
    except WebSocketDisconnect:
        room.disconnect(player)
        await room.broadcast(f"{player_name} left the game.")


@app.websocket("/ws/{player_name}/create-room")
async def create_room(websocket: Player, player_name: str, room_name: str, **kwargs):
    try:
        room: Room = await rooms_manager.create_room(room_name=room_name, kwargs=kwargs)
        join_room(websocket, player_name, room_id=room.id)
    except WebSocketDisconnect:
        websocket.close(reason=f"Could not create room.")
