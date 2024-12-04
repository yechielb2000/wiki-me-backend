from fastapi import HTTPException
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send

from app.models.player import Player


class PlayerSessionMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in ("http", "websocket"):
            headers = Headers(scope=scope)
            player_id = headers.get('Player-ID')  # TODO should I use my own header or cookies?
            if not player_id or not Player.exists(player_id):
                raise HTTPException(status_code=401, detail="Session expired or does not exist")
            scope['player_id'] = player_id  # Does this work?

        await self.app(scope, receive, send)
