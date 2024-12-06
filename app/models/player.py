from app.models.base_redis_entity import BaseRedisEntity


class Player(BaseRedisEntity):
    admin: bool = False
    name: str
