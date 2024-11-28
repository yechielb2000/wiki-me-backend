import os
from dataclasses import dataclass

from redis import Redis


# TODO: change configuration between prod and integ
@dataclass
class RedisConfig:
    host: str = os.environ.get('REDIS_ADDRESS', '0.0.0.0')
    port: int = os.environ.get('REDIS_PORT', 6379)


redis_client = Redis(
    host=RedisConfig.host,
    port=RedisConfig.port,
    decode_responses=True,
    ssl=True
)
