import logging
import os

from flask import Flask
from logging.handlers import RotatingFileHandler
os.environ['FLASK_APP'] = 'Pi_Car.app'


def create_app(confi_file="config/local_config.py"):
    app = Flask(__name__)  # Initialize the app
    app.config.from_pyfile(confi_file, silent=False)  # Read in config from file

    # Configure file-based log handler
    log_file_handler = RotatingFileHandler(
        filename=app.config.get("LOG_FILE_NAME", "config/pi-car.log"),
        maxBytes=10000000,
        backupCount=4,
    )
    log_file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
    app.logger.addHandler(log_file_handler)
    app.logger.setLevel(app.config.get("LOGGER_LEVEL", "ERROR"))
    app.logger.info("---- STARTING APP ----")

    @app.route("/")
    def hello_world():
        app.logger.info("Running first route")
        return "Hello, World"

    app.logger.info("----- FINISHED STARTING APP -----")
    return app