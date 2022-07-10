"""
This is the listener to which the module boilerplate would POST to.
The data received by the listener is written to json file.
"""

from logging import basicConfig, DEBUG, getLogger
from os import getenv, path, remove
from bottle import run, post, request
from json import dumps
from signal import signal, SIGTERM


@post("/")
def request_handler():

    output_file = getenv("OUTPUT_FILE")

    received_data = dumps(request.json, indent=4)
    log.info("The received data: %s", received_data)

    with open(output_file, "w") as outfile:
        outfile.write(received_data)

def teardown_and_exit(*args):
    del args
    output_file = getenv("OUTPUT_FILE")
    if path.exists(output_file):
        remove(output_file)
    exit(0)

if __name__ == "__main__":
    signal(SIGTERM, teardown_and_exit)

    basicConfig(
        level=DEBUG,
        format="{'level': '%(levelname)s', 'time': '%(asctime)s', 'filename': '%(name)s', 'message': '%(message)s'}",
    )

    log = getLogger("main")

    log.info(
        "Listener running on %s at port %s",
        getenv("HOST"),
        getenv("PORT"),
    )

    # start the server
    run(
        host=getenv("HOST"),
        port=getenv("PORT"),
        quiet=True,
    )
