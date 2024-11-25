import datetime

from fastapi import WebSocket
from loguru import logger


class Player:
    def __init__(self, websocket: WebSocket, player_id: str):
        self.websocket = websocket
        self.player_id = player_id
        self.connected_at = datetime.datetime.now(tz=datetime.UTC)
        self.logger = logger.bind(player_id=player_id)

    async def connect(self):
        """Handle player connection."""
        self.logger.debug(f'player is connecting...')
        await self.websocket.accept()
        self.logger.success(f'player is connected.')

    async def disconnect(self):
        """Handle player disconnection."""
        self.logger.debug(f'player is disconnecting...')
        await self.websocket.close()
        self.logger.success(f'player has been disconnected.')

    async def send_message(self, message: str):
        """Send a message to the player's WebSocket."""
        await self.websocket.send_text(message)

    async def receive_message(self) -> str:
        """Receive a message from the player's WebSocket."""
        return await self.websocket.receive_text()
