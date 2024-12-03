from flask import Flask
from flask_cors import CORS
import os

from db_service.config import DB_Config
from db_service.db import DB_Client
from models.base import Base
from routes import register_routes

def initialise_app():
    """
    Initialises app instance
    """
    # deleting any pre-existing db instance
    app_db_path = os.path.join(os.path.dirname(__file__), "app.db")
    if os.path.exists(app_db_path):
        os.remove(app_db_path)
    
    # initialising flask app
    app = Flask(__name__)
    CORS(app)

    # app configuration
    app.config.from_object(DB_Config)

    # Initialize DB client
    db_client = DB_Client()

    # create table if they do not exist
    with app.app_context():
        Base.metadata.create_all(db_client.session.bind)
    
    # register blueprints
    register_routes(app=app)

    return app

if __name__ == "__main__":
    app = initialise_app()
    app.run(debug=True)