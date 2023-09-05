from fastapi import WebSocket
import uuid


class Room:
    def __init__(
        self,
        name: str,
        id: str = str(uuid.uuid4()),
        game_rounds: int = 3,
        max_connections_allowed: int = 10,
        wikis_to_change_per_round: int = 0,
        time_to_wait_between_rounds: int = 30,
    ):
        self.name = name
        self.id = id
        self.game_rounds = game_rounds
        self.wikis_to_change_per_round = wikis_to_change_per_round
        self.time_to_wait_between_rounds = time_to_wait_between_rounds
        self.max_connections_allowed = max_connections_allowed
        self.active_connections: list[WebSocket] = list()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def is_admin(self, websocket: WebSocket) -> bool:
        return websocket == self.active_connections[0]

    def set_random_id(self) -> str:
        self.id = str(uuid.uuid4())
