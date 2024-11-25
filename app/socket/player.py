import datetime

from fastapi import WebSocket


class Player:
    def __init__(self, websocket: WebSocket, player_id: str):
        self.websocket = websocket
        self.player_id = player_id
        self.connected_at = datetime.datetime.now(tz=datetime.UTC)

    async def send_message(self, message: str):
        """Send a message to the player's WebSocket."""
        await self.websocket.send_text(message)

    async def receive_message(self) -> str:
        """Receive a message from the player's WebSocket."""
        return await self.websocket.receive_text()

    async def disconnect(self):
        """Handle player disconnection."""
        await self.websocket.close()
