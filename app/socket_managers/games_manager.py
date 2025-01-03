from typing import Dict, List

from loguru import logger

from app.exceptions import GameNotFound
from app.socket_managers.game_room import GameRoom


class GamesManager:
    def __init__(self) -> None:
        self._active_games: Dict[str, GameRoom] = dict()

    @property
    def games(self) -> Dict[str, GameRoom]:
        return self._active_games

    @property
    def games_ids(self) -> List[str]:
        return list(self._active_games.keys())

    def get_game_manager(self, game_id: str) -> GameRoom:
        game = self._active_games.get(game_id)
        if not game:
            raise GameNotFound(game_id)
        return game

    def add_game_manager(self, game_manager: GameRoom) -> None:
        # TODO: we want to save active games in redis
        while game_manager.game.id in self.games_ids:
            game_manager.game.generate_new_id()
            # TODO: check if new id is replacing older id
        self._active_games[game_manager.game.id] = game_manager

    def remove_game_manager(self, game_id: str):
        game = self.get_game_manager(game_id)
        if game:
            logger.success(f'game {game} has been removed')
            del self._active_games[game_id]

    def game_exists(self, room_id: str) -> bool:
        return bool(self._active_games.get(room_id, False))
