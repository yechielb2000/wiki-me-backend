from typing import Dict, List
from loguru import logger
from app.exceptions import GameNotFound
from app.socket.game_manager import GameManager


class GamesManager:
    def __init__(self) -> None:
        self._active_games: Dict[str, GameManager] = dict()

    @property
    def games(self) -> Dict[str, GameManager]:
        return self._active_games

    @property
    def games_ids(self) -> List[str]:
        return list(self._active_games.keys())

    def get_game(self, game_id: str) -> GameManager:
        game = self._active_games.get(game_id)
        if not game:
            raise GameNotFound(game_id)
        return game

    def game_exists(self, room_id: str) -> bool:
        return bool(self._active_games.get(room_id, False))

    def add_game(self, game: GameManager) -> None:
        while game.id in self.games_ids:
            game.generate_id()
        self._active_games[game.id] = game

    def remove_game(self, game_id: str):
        game = self.get_game(game_id)
        if game:
            logger.debug(f'game {game} has been removed')
            del self._active_games[game_id]
