import json
from typing import Dict

from loguru import logger

from app.models.game import Game
from app.socket_managers.player_connection import PlayerConnection


class GameRoom:
    def __init__(self, game: Game):
        self._game = game
        self._connections: Dict[str, PlayerConnection] = dict()
        self._logger = logger.bind(game_id=game.id)

    @property
    def game(self) -> Game:
        return self._game

    @property
    def connections(self) -> Dict[str, PlayerConnection]:
        return self._connections

    def get_player(self, player_id: str) -> PlayerConnection:
        # TODO: handle player doesn't exists
        return self._connections[player_id]

    def add_player(self, connection: PlayerConnection):
        self._connections[connection.player.id] = connection
        self._logger.info(f'player {connection.player.id} added.')

    async def remove_player(self, player_id: str):
        self._connections.pop(player_id, None)
        self._logger.info(f'player {player_id} removed.')

    async def send_personal_message(self, message: str, player_id: str):
        connection = self.get_player(player_id)
        await connection.send_message(message)

    async def broadcast(self, message: str):
        for connection in self._connections.values():
            await connection.send_message(message)

    def get_game_admin(self) -> PlayerConnection:
        return list(filter(lambda player: player.admin, self._connections.values()))[0]

    def has_reached_connections_limit(self) -> bool:
        return len(self._connections.keys()) == self._game.max_connections

    def round(self):
        """
        Manage round flow. get new points and send them to clients.
        Then wait to get the first user to arrive.
        First user to send an update is won because the client triggered when the right wiki id pops up,
        then it tells the server that he arrived.
        """
        start_point, end_point = next(self.game.get_rounds_points())  # should use next?
        points = json.dumps(dict(startpoint=start_point.model_dump(), endpoint=end_point.model_dump()))
        self.broadcast(points)
        while True:
            # TODO when going out of wiki scope raise an exception and return him to the last page
            # TODO: use redis pub/sub for managing users updates
            # push_handler_func
            pass
