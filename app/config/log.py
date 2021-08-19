"""logging configurations"""
from logging import basicConfig, DEBUG


def configure_logging():
    basicConfig(
        level=DEBUG, format='➡️  %(levelname)s : %(asctime)s : %(name)s  :  %(message)s')
