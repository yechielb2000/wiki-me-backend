from loguru import logger
from pydantic import BaseModel

from app.services.connections import redis_client


class WikiBaseModel(BaseModel):
    id: str = None

    def __pydantic_init_subclass__(self):
        self.id = redis_client.incr(f"{self.__class__.__name__}:id")  # is this suppose to be async?
        self._logger = logger.bind(id=self.id, cls=self.__class__.__name__)

    @property
    def logger(self):
        return self._logger

    @property
    def redis_key(self) -> str:
        return f"{self.__class__.__name__}:{self.id}"

    def save_to_redis(self):
        """Save model fields to Redis."""
        self.logger.info(f"Saving model fields to redis")
        redis_client.set(self.redis_key, self.model_dump())

    def delete_from_redis(self):
        """Delete the model from Redis."""
        self.logger.info(f"Deleting model fields from redis")
        redis_client.delete(self.redis_key)

    @classmethod
    def load_from_redis(cls, model_id: str):
        """Load the model from Redis."""
        redis_key = f"{cls.__name__}:{model_id}"
        logger.info(f"Loading model fields from redis", model_id=model_id, model_name=cls.__name__)
        data = redis_client.get(redis_key)
        if not data:
            raise ValueError(f"No data found in Redis for key {redis_key}")
        return cls.model_validate_json(data)

    def __str__(self) -> str:
        return self.redis_key
