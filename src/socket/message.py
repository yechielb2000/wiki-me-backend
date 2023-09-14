import json
from pydantic import BaseModel
from src.services import Wiki


class MessageTypes:
    WIN = "win"
    PLAY = "play"
    SYSTEM = "system"
    MESSAGE = "message"
    DISCONNECT_ALL = "disconnect_all"
    DISCONNECT = "disconnect"
    REMOVE = "remove"
    ERROR = "error"


class SocketMessage(BaseModel):
    message_type: str
    message: str
    wiki_start_point: Wiki.WikiPage
    wiki_endpoint: Wiki.WikiPage


def load_json(data: str) -> SocketMessage:
    return json.loads(data, object_hook=lambda x: SocketMessage.model_validate(x))
