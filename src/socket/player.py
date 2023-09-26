from fastapi import WebSocket


class Player(WebSocket):
    def __init__(self, name: str = None) -> None:
        self.name = name

    def set_name(self, name: str) -> None:
        self.name = name
