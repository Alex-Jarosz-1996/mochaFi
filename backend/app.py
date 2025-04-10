from flask import Flask
from flask_cors import CORS
import os

from db_service.config import DB_Config
from db_service.db import DB_Client
from models.base import Base
from routes import register_routes
from setup_logging.setup_logging import logger

def initialise_app():
    """
    Initialises app instance
    """
    logger.info("Deleting any pre-existing db instance.")
    app_db_path = os.path.join(os.path.dirname(__file__), "app.db")
    if os.path.exists(app_db_path):
        os.remove(app_db_path)
    
    logger.info("Initialising flask app.")
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    CORS(app)

    logger.info("App configuration.")
    app.config.from_object(DB_Config)

    logger.info("Initialize DB client.")
    db_client = DB_Client()

    logger.info("Create table if they do not exist.")
    with app.app_context():
        Base.metadata.create_all(db_client.session.bind)
    
    logger.info("Register route blueprints.")
    register_routes(app=app)

    return app

if __name__ == "__main__":
    logger.info("Initialising app.")
    app = initialise_app()

    logger.info("Running app.")
    app.run(host='0.0.0.0', debug=True)
