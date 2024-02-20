import logging
import os
import sys

from flask import Flask
from flask_cors import CORS

from app import jwt_handlers
from app.extensions import database, jwt
from app.routes.applications_route import applications_bp
from app.routes.error_handler import handle_all_unhandled_exceptions


def create_app() -> Flask:
    """
    Creates and configures the Flask application.

    This function creates a new Flask application, configures it from a
    configuration file, sets up CORS, logging, extensions, and registers
    blueprints. Also sets up a global error handler for unhandled exceptions.

    :returns: The configured Flask application.
    """

    recruiter_api = Flask(__name__)
    recruiter_api.config.from_pyfile('config.py')
    recruiter_api.errorhandler(Exception)(handle_all_unhandled_exceptions)

    CORS(recruiter_api, resources={r"/api/*": {"origins": "*"}})

    setup_logging(recruiter_api)
    setup_extensions(recruiter_api)
    register_blueprints(recruiter_api)

    return recruiter_api


def setup_logging(recruiter_api: Flask) -> None:
    """
    Sets up logging for the Flask application.

    This function checks if LOG_TO_STDOUT is enabled in the configuration. If so,
    it sets up logging to stdout. Otherwise, it configures logging to a file as
    previously.

    :param recruiter_api: The Flask application.
    """

    if recruiter_api.config.get('LOG_TO_STDOUT'):
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(
                recruiter_api.config.get('LOG_LEVEL', logging.INFO))
        stream_handler.setFormatter(logging.Formatter(
                recruiter_api.config.get(
                        'LOG_FORMAT',
                        '%(asctime)s - %(name)s - '
                        '%(levelname)s - %(message)s')))
        logging.getLogger().addHandler(stream_handler)
    else:
        log_dir = recruiter_api.config.get('LOG_DIR', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(
                recruiter_api.config.get('LOG_FILE',
                                         os.path.join(log_dir, 'app.log')))
        file_handler.setLevel(
                recruiter_api.config.get('LOG_LEVEL', logging.INFO))
        file_handler.setFormatter(logging.Formatter(
                recruiter_api.config.get(
                        'LOG_FORMAT',
                        '%(asctime)s - %(name)s - '
                        '%(levelname)s - %(message)s')))
        logging.getLogger().addHandler(file_handler)

    logging.getLogger().setLevel(
            recruiter_api.config.get('LOG_LEVEL', logging.INFO))


def setup_extensions(recruiter_api: Flask) -> None:
    """
    Sets up extensions for the Flask application.

    This function initializes the database and JWT extensions for the Flask
    application, and registers JWT error handlers. It also creates all
    database tables.

    :param recruiter_api: The Flask application.
    """

    database.init_app(recruiter_api)
    jwt.init_app(recruiter_api)
    jwt_handlers.register_jwt_handlers(jwt)

    with recruiter_api.app_context():
        database.create_all()


def register_blueprints(recruiter_api: Flask) -> None:
    """
    Registers blueprints for the Flask application.

    This function registers blueprints for the Flask application. Each
    blueprint corresponds to a different part of the application.

    :param recruiter_api: The Flask application.
    """

    recruiter_api.register_blueprint(
            applications_bp, url_prefix='/api/applications')


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

application = create_app()
