import logging

from loguru import logger

from app.services.connections import elastic_client


class ElasticHandler(logging.Handler):

    def __init__(self, elastic):
        super().__init__()
        self.elastic = elastic

    def emit(self, record):
        # TODO: build a well structured schema for all logs
        self.elastic.index(index='app-logs', doc_type='log', body=record.__dict__)


def setup_logger():
    logger.add(ElasticHandler(elastic_client), format='{message}')
