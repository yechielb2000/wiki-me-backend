from app.models.redis_actions import RedisActions


class Player(RedisActions):
    admin: bool = False
    name: str
