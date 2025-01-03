from elasticsearch import Elasticsearch
from redis.asyncio.client import Redis

from app.services.env_vars import *

__all__ = [
    'redis_client',
    'elastic_client'
]

redis_client = Redis(host=REDIS_ADDRESS, port=REDIS_PORT, decode_responses=True)

elastic_client = Elasticsearch(f'{ELASTICSEARCH_ADDRESS}:{ELASTICSEARCH_PORT}')
