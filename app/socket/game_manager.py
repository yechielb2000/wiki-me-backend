from typing import Dict

from loguru import logger

from app.models.game import Game
from app.socket.player import Player


class GameManager:
    def __init__(self, game: Game, player: Player):
        self._game = game
        self._players: Dict[str, Player] = dict()

    @property
    def game(self) -> Game:
        return self.game

    @property
    def players(self) -> Dict[str, Player]:
        return self._players

    async def connect(self, player: Player):
        await player.connect()
        self._players[player.player_id] = player

    async def disconnect(self, player: Player):
        await player.disconnect()
        del self._players[player.player_id]

    async def send_personal_message(self, message: str, player: Player):
        # TODO: this should be implemented a little different
        await player.websocket.send_text(message)

    async def broadcast(self, message: str):
        for player in self._players.values():
            await player.websocket.send_text(message)

    async def is_admin(self, player: Player) -> bool:
        # TODO: does game needs an admin? (settings can't be changed anyway)
        return False
