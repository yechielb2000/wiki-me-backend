import os

from redis import Redis

redis_client = Redis(
    host=os.environ.get('REDIS_ADDRESS', '0.0.0.0'),
    port=os.environ.get('REDIS_PORT', 6379),
    decode_responses=True,
    ssl=True
)
