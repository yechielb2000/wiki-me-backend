from fastapi import WebSocket, WebSocketException

from app.services.connections import redis_client

COOKIE_NAME = "client_cookie"


async def websocket_validate_api_key(websocket: WebSocket):
    api_key = websocket.cookies.get(COOKIE_NAME)
    if not api_key or not redis_client.exists(api_key):
        await websocket.close(code=WebSocket)
        raise ValueError("Invalid WebSocket API Key")
    return api_key
