from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_service.config import DB_Config

class DB_Client:
    def __init__(self):
        engine = create_engine(DB_Config.SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=engine)
        self.session = Session()
