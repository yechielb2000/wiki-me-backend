from datetime import timedelta
from typing import Annotated

from pydantic import Field

from app.models.base_model import WikiBaseModel


class Game(WikiBaseModel):
    name: str
    game_rounds: Annotated[int, Field(3, gt=0, le=5)]
    max_connections: Annotated[int, Field(3, gt=0, le=10)]
    wait_between_rounds: Annotated[timedelta, Field(ge=3, lt=30)]
    round_duration: Annotated[timedelta, Field(gt=120, le=300)]

    @property
    def url(self) -> str:
        return f'/game/{self.id}'  # TODO: add domain and route from env variable
