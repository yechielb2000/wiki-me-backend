import json
from fastapi import FastAPI, WebSocketDisconnect
from src.services import Wiki
from src.socket import Player, Room
from src.socket.message import MessageTypes, load_json
from .rooms_manager import RoomsManager

app = FastAPI()
rooms_manager: RoomsManager = RoomsManager()


@app.websocket("/ws/{player_name}")
async def join_room(player: Player, player_name: str, room_id: str):
    player.set_name(player_name)
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
            data = load_json(await player.receive_text())
            if data.message_type == MessageTypes.PLAY:
                wiki = Wiki()
                data.wiki_start_point = wiki.start_point
                data.wiki_endpoint = wiki.end_point
                await room.broadcast(data.model_dump_json())
                while True:
                    data = load_json(await player.receive_text())
                    if data.message_type == MessageTypes.WIN:
                        data.message = f"{player.name} has won!"
                        await room.broadcast(data.model_dump_json())
                        break
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
