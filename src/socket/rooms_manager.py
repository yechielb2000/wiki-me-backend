from src.socket.room import Room


class RoomsManager:
    def __init__(self) -> None:
        self.active_rooms: list[Room] = list()

    def room_exists(self, room: Room) -> bool:
        return room in self.active_rooms

    async def create_room(self, room_name: str, **kwargs) -> None:
        room = Room(room_name, **kwargs)
        while self.id_exists(room):
            room.set_random_id()
        await self.active_rooms.append(room)

    def remove_room(self, room: Room):
        if self.room_exists(room):
            self.active_rooms.remove(room)

    def id_exists(self, room: Room) -> bool:
        for active_room in self.active_rooms:
            if room.id == active_room.id:
                return True
        return False
