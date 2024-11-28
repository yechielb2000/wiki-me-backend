import logging


class ElasticHandler(logging.Handler):

    def __init__(self, eck):
        super().__init__()
        self.eck = eck

    def emit(self, record):
        self.


def setup_logger():

