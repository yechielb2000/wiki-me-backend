from typing import Union
from src.socket.player import Player
import uuid


class Room:
    def __init__(
        self,
        name: str,
        id: str = str(uuid.uuid4()),
        game_rounds: int = 3,
        max_players_allowed: int = 10,
        wikis_to_change_per_round: int = 0,
        time_to_wait_between_rounds: int = 30,
    ):
        self.name = name
        self.id = id
        self.game_rounds = game_rounds
        self.wikis_to_change_per_round = wikis_to_change_per_round
        self.time_to_wait_between_rounds = time_to_wait_between_rounds
        self.max_players_allowed = max_players_allowed
        self.active_players: list[Player] = list()

    async def connect(self, player: Player):
        await player.accept()
        self.active_players.append(player)

    def disconnect(self, player: Player):
        # Probably should close session first
        self.active_players.remove(player)

    def disconnect_all(self):
        self.active_players.clear()

    async def broadcast(self, message: str):
        for player in self.active_players:
            await player.send_text(message)

    async def is_admin(self, player: Player) -> bool:
        return player == self.active_players[0]

    def set_random_id(self) -> str:
        self.id = str(uuid.uuid4())

    def get_player_if_exists(self, player_name: str) -> Union[Player, None]:
        for active_player in self.active_players:
            if player_name == active_player.name:
                return active_player
        return None
