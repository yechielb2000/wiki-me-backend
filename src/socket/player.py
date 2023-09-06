from fastapi import WebSocket
from starlette.types import Receive, Scope, Send


class Player(WebSocket):
    def __init__(self, scope: Scope, receive: Receive, send: Send, name: str = None) -> None:
        super().__init__(scope, receive, send)
        self.name = name

    def set_name(self, name: str):
        self.name = name