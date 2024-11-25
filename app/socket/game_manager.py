from typing import Dict
from venv import logger

from app.models.game import Game
from app.socket.player import Player


class GameManager:
    def __init__(self, game: Game):
        self._game = game
        self._players: Dict[str, Player] = dict()

    @property
    def game(self) -> Game:
        return self.game

    @property
    def players(self) -> Dict[str, Player]:
        return self._players

    async def connect(self, player: Player):
        logger.debug(f'player {player} is connecting...')
        await player.websocket.accept()
        logger.info(f'player {player} has been connected')
        self._players[player.player_id] = player

    async def disconnect(self, player: Player):
        logger.debug(f'player {player} is disconnecting')
        await player.websocket.close()
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
