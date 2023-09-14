from pydantic import BaseModel
from src.services.wiki import Wiki


class MessageTypes:
    WIN = "win"
    PLAY = "play"
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
