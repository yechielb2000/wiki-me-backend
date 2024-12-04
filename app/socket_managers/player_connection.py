from fastapi import WebSocket
from loguru import logger

from app.models.player import Player


class PlayerConnection:
    def __init__(self, websocket: WebSocket, player: Player):
        self._player = player
        self._websocket = websocket
        self._logger = logger.bind(player_id=self.player.id)

    @property
    def logger(self):
        return self._logger

    @property
    def player(self) -> Player:
        return self._player

    async def connect(self):
        """Handle player connection."""
        self.logger.debug('player is connecting...')
        await self._websocket.accept()
        self.logger.success('player is connected.')

    async def disconnect(self):
        """Handle player disconnection."""
        self.logger.debug('player is disconnecting...')
        await self._websocket.close()
        self.logger.success('player has been disconnected.')

    async def send_message(self, message: str):
        """Send a message to the player's WebSocket."""
        await self._websocket.send_text(message)

    async def receive_message(self) -> str:
        """Receive a message from the player's WebSocket."""
        return await self._websocket.receive_text()
