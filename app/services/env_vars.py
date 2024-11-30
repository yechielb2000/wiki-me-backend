import os

__all__ = [
    'REDIS_ADDRESS',
    'REDIS_PORT',
    'ELASTICSEARCH_ADDRESS',
    'ELASTICSEARCH_PORT'
]

# Redis stack server
REDIS_ADDRESS = os.environ.get('REDIS_ADDRESS', '127.0.0.1')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

# Elasticsearch
ELASTICSEARCH_ADDRESS = os.environ.get('ELASTICSEARCH_URL', 'http://localhost')
ELASTICSEARCH_PORT = os.environ.get('ELASTICSEARCH_PORT', 9200)
