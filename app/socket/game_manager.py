import json
from typing import Dict

from loguru import logger
from wikipedia import wikipedia

from app.models.game import Game
from app.socket.player import Player


class GameManager:
    def __init__(self, game: Game):
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

    def add_player(self, player: Player):
        # TODO: should check player if already in?
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

    def has_reached_connections_limit(self) -> bool:
        return len(self._players.keys()) == self._game.max_players

    def round(self):
        """
        Manage round flow. get new points and send them to clients.
        Then wait to get the first user to arrive.
        First user to send an update is won because the client triggered when the right wiki id pops up,
        then it tells the server that he arrived.
        """
        points = self.get_new_points()
        self.broadcast(points)
        while True:
            # TODO when going out of wiki scope raise an exception and return him to the last page
            # TODO: use redis pub/sub for managing users updates
            #push_handler_func
            pass

    def get_new_points(self) -> str:
        """
        :return: new start point wiki title. new destination wiki title.
        """
        return json.dumps(dict(start_point=wikipedia.random(), end_point=wikipedia.random()))
