import uuid

from fastapi import WebSocket


class Game:
    def __init__(
            self,
            name: str,
            game_rounds: int = 3,
            max_connections_allowed: int = 10,
            wikis_to_change_per_round: int = 0,
            time_to_wait_between_rounds: int = 30,
    ):
        self.name = name
        self.game_rounds = game_rounds
        self.wikis_to_change_per_round = wikis_to_change_per_round
        self.time_to_wait_between_rounds = time_to_wait_between_rounds
        self.max_connections_allowed = max_connections_allowed
        self.active_connections: list[WebSocket] = list()

        self.generate_id()

    @property
    def id(self) -> str:
        return self._id

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

    def generate_id(self):
        self._id = str(uuid.uuid4())

    def __str__(self) -> str:
        return f'[name: {self.name} | id: {self.id}]'
