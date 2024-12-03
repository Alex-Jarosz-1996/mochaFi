import os

class DB_Config:
    """
    Class responsible for db config.
    Currently, app uses sqlite as the db.
    """
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False