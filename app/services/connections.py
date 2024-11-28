from elasticsearch import Elasticsearch
from redis import Redis

from app.services.env_vars import *
from app.services.env_vars import ELASTICSEARCH_ADDRESS, ELASTICSEARCH_PORT

redis_client = Redis(
    host=REDIS_ADDRESS,
    port=REDIS_PORT,
    decode_responses=True,
    ssl=True
)

elastic_client = Elasticsearch(f'{ELASTICSEARCH_ADDRESS}:{ELASTICSEARCH_PORT}')
