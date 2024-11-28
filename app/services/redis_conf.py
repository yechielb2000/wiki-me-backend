from dataclasses import dataclass

from redis import Redis

import os

# TODO: change configuration between prod and integ
@dataclass
class RedisConfig:
    address: str = os.environ.get('REDIS_ADDRESS', '0.0.0.0')
    port: int = os.environ.get('REDIS_PORT', 6379)
