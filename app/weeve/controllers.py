"""
All route entry points
"""
from flask import Flask, request

from app.config import HTTP_CODES
from app.module import data_validation, module_main

from .egress import send_data
from .health import health_check


def stat_routes(app: Flask):
    """Sets the health route of the application

    Args:
        app (Flask): [Flask library]

    """
    @app.route('/health', methods=["GET"])
    def health():
        return health_check(), HTTP_CODES['OK']


def main_routes(app: Flask):
    """Sets the main application routes

    Args:
        app (Flask): [Flask library]
    """
    @app.route('/', methods=["POST"])
    def handle():
        received_data = request.get_json(force=True)

        parsed_data, err = data_validation(received_data)

        if err:
            app.logger.error('Error: %s', err)
            return err, HTTP_CODES['BAD_REQUEST']

        module_output, err = module_main(parsed_data)

        if err:
            app.logger.error('Error: %s', err)
            return err, HTTP_CODES['INTERNAL_SERVER_ERROR']

        if not module_output:
            return "", HTTP_CODES['NO_CONTENT']

        app.logger.error("Error while transfering")
        return "Error while transfering", HTTP_CODES['INTERNAL_SERVER_ERROR']
