import json
from typing import Any
from fastapi import FastAPI, WebSocketDisconnect
from src.services.wiki import Wiki
from src.socket import Player, Room, RoomsManager, SocketMessage, MessageTypes


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
            data = await player.receive_text()
            data: SocketMessage = load_json(data)
            if data.message_type == MessageTypes.PLAY:
                wiki = Wiki()
                data.wiki_start_point = wiki.start_point
                data.wiki_endpoint = wiki.end_point
                await room.broadcast(data.model_dump_json())
                while True:
                    data = await player.receive_text()
                    data: SocketMessage = load_json(data)
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


def load_json(data: Any) -> SocketMessage:
    return json.loads(data, object_hook=lambda x: SocketMessage.model_validate(x))
