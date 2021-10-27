"""logging configurations"""
from logging import basicConfig, DEBUG


def configure_logging():
    basicConfig(
        level=DEBUG, format="{'levelname': '%(levelname)s', 'asctime': '%(asctime)s', 'name': '%(name)s', 'message': '%(message)s'}")
