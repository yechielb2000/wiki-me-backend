class GameNotFound(Exception):
    """game not found"""
    def __init__(self, game_id: str):
        self.add_note(f"game id: {game_id}")