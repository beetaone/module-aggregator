"""Main app file"""
from logging import getLogger
from app import create_app
from app.config import WEEVE, configure_logging

from app.module import frequency_processing, set_module_app

log = getLogger("main")


def main():
    """ Main app entry point"""
    configure_logging()
    log.info("%s Started", WEEVE["MODULE_NAME"])
    app = create_app()
    set_module_app(app)

    # start processing interval
    frequency_processing()

    app.run(host=WEEVE['INGRESS_HOST'], port=WEEVE["INGRESS_PORT"])


if __name__ == "__main__":
    main()
