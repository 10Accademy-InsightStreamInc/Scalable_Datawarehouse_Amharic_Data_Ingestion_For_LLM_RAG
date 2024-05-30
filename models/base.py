from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os,sys



from dotenv import load_dotenv

load_dotenv()
rpath = os.path.abspath('../api')
SQLALCHEMY_DATABASE_URL = os.getenv('DB_CONNECTION_STRING')

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self, database_url: str =SQLALCHEMY_DATABASE_URL  ):
        self.database_url = database_url
        self.engine = create_engine(
            self.database_url, connect_args={},pool_pre_ping=True,pool_recycle=300
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_base(self):
        return self.Base

    def get_session_local(self):
        return self.SessionLocal