from datetime import timedelta
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field


class Game(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    game_rounds: Annotated[int, Field(3, gt=0, le=5)]
    max_connections: Annotated[int, Field(3, gt=0, le=10)]
    wait_between_rounds: Annotated[timedelta, Field(ge=3, lt=30)]
    round_duration: Annotated[timedelta, Field(gt=120, le=300)]

    def generate_new_id(self):
        """
        for case that this uuid is already taken
        """
        self.id = str(uuid4())

    def __str__(self) -> str:
        return f'[name: {self.name} | id: {self.id}]'

    @property
    def url(self) -> str:
        return f'/game/{self.id}'  # TODO: add domain and route from env variable
