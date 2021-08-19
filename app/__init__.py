"""
Main flask entry point
"""
from logging import getLogger
from flask import Flask

from app.config import WEEVE
from app.weeve import main_routes, stat_routes

log = getLogger(__name__)


def create_app() -> Flask:
    """ Configures the flask ap and returns it

    Returns:
        Flask: [Flask app]
    """
    app = Flask(__name__)
    set_routes(app)
    log.info('%s Web Server Initialise"', WEEVE['MODULE_NAME'])
    return app


def set_routes(app: Flask):
    """ Sets routs for the flask app

    Args:
        app (Flask): [Flask]
    """
    stat_routes(app)
    main_routes(app)
