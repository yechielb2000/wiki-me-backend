from datetime import timedelta
from typing import Annotated, List

import wikipedia
from pydantic import Field, BaseModel, field_validator

from app.models.base_redis_entity import BaseRedisEntity


class Rounds(BaseModel):
    start_point: str
    end_point: str


class Game(BaseRedisEntity):
    name: str
    rounds_count: Annotated[int, Field(3, gt=0, le=5)]
    max_connections: Annotated[int, Field(3, gt=0, le=10)]
    wait_between_rounds: Annotated[timedelta, Field(ge=3, lt=30)]
    round_duration: Annotated[timedelta, Field(gt=120, le=300)]
    rounds: List[Rounds] | None = Field(default_factory=list(), gt=0)

    @property
    def url(self) -> str:
        # This will not be necessary
        return f'/game/{self.id}'  # TODO: add domain and route from env variable

    @classmethod
    @field_validator('rounds', 'rounds_count')
    def generate_rounds(cls, rounds, rounds_count):
        """ Get start and end points of each game round. """
        rounds_titles = iter(wikipedia.random(pages=rounds_count * 2))
        for start_point, end_point in zip(rounds_titles, rounds_titles):
            rounds.append(Rounds(start_point=start_point, end_point=end_point))
        return rounds

    def get_rounds_points(self):
        """ Per round yield its current start and end points. """
        rounds = iter(self.rounds)
        for start_point, end_point in zip(rounds, rounds):
            yield start_point, end_point
