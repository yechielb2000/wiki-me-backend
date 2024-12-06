import json
from datetime import timedelta

from loguru import logger
from pydantic import BaseModel
from redis.typing import ExpiryT

from app.services.connections import redis_client


class RedisActions(BaseModel):
    id: str

    def __init__(self, /, **data: any) -> None:
        super().__init__(**data)
        self._logger = logger.bind(id=self.id, cls=self.__class__.__name__)

    @classmethod
    async def generate_id(cls) -> str:
        """ Generate a unique id in redis for this model. """
        return str(await redis_client.incr(f"{cls.__name__}:id"))

    @property
    def redis_key(self) -> str:
        return f"{self.__class__.__name__}:{self.id}"

    async def create(self, ex: ExpiryT = timedelta(hours=1)):
        """Save model fields to Redis."""
        if not self.id:
            self.id = await self.generate_id()
        self._logger.info("Saving model fields to redis")
        await redis_client.set(self.redis_key, json.dumps(self.model_dump()), ex=ex)

    async def delete(self):
        """Delete the model from Redis."""
        self._logger.info("Deleting model fields from redis")
        await redis_client.delete(self.redis_key)

    @classmethod
    async def get(cls, model_id: str):
        """Load the model from Redis."""
        redis_key = f"{cls.__name__}:{model_id}"
        logger.info("Loading model fields from redis", model_id=model_id, model_name=cls.__name__)
        data = await redis_client.get(redis_key)
        if not data:
            raise ValueError(f"No data found in Redis for key {redis_key}")
        return cls.model_validate_json(data)

    @classmethod
    async def update(cls, model_id: str, data: dict):
        redis_key = f"{cls.__name__}:{model_id}"
        logger.info("Updating model fields from redis", model_id=model_id, data=data, model_name=cls.__name__)
        redis_client.set(redis_key, json.dumps(data))
        return cls.model_validate(data)

    @classmethod
    async def exists(cls, model_id: str) -> bool:
        redis_key = f"{cls.__name__}:{model_id}"
        return redis_client.exists(redis_key)

    def __str__(self) -> str:
        return f'{self.__class__.__name__}:{self.redis_key}'
