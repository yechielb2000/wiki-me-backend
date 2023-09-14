from typing import Union
from src.socket.room import Room


class RoomsManager:
    def __init__(self) -> None:
        self.active_rooms: list[Room] = list()

    async def create_room(self, room_name: str, **kwargs) -> Room:
        room = Room(room_name, **kwargs)
        while self.get_room_if_exists(room.id):
            room.set_random_id()
        await self.active_rooms.append(room)
        return room

    def remove_room(self, room: Room):
        if self.get_room_if_exists(room.id):
            room.disconnect_all()
            self.active_rooms.remove(room)

    def get_room_if_exists(self, room_id: str) -> Union[Room, None]:
        for active_room in self.active_rooms:
            if room_id == active_room.id:
                return active_room
        return None
