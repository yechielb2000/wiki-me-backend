from elasticsearch import Elasticsearch
from redis import Redis

from app.services.env_vars import *

__all__ = [
    'redis_client',
    'elastic_client'
]

redis_client = Redis(
    host=REDIS_ADDRESS,
    port=REDIS_PORT,
    decode_responses=True,
    ssl=True
)

elastic_client = Elasticsearch(f'{ELASTICSEARCH_ADDRESS}:{ELASTICSEARCH_PORT}')
