from typing import Dict

from loguru import logger

from app.models.game import Game
from app.socket.player import Player


class GameManager:
    def __init__(self, game: Game, player: Player):
        self._game = game
        self._players: Dict[str, Player] = dict()
        self.logger = logger.bind(game_id=game.game_id)

    @property
    def game(self) -> Game:
        return self.game

    @property
    def players(self) -> Dict[str, Player]:
        return self._players

    def get_player(self, player_id: str) -> Player:
        # TODO: handle player doesn't exists
        return self._players[player_id]

    async def add_player(self, player: Player):
        self._players[player.player_id] = player
        self.logger.info(f'player {player.player_id} added.')

    async def remove_player(self, player_id: str):
        self._players.pop(player_id, None)
        self.logger.info(f'player {player_id} removed.')

    async def send_personal_message(self, message: str, player_id: str):
        player = self.get_player(player_id)
        await player.websocket.send_text(message)

    async def broadcast(self, message: str):
        for player in self._players.values():
            await player.websocket.send_text(message)

    async def is_admin(self, player: Player) -> bool:
        # TODO: does game needs an admin? (settings can't be changed anyway)
        return False
