from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

import os

from dotenv import load_dotenv

load_dotenv()

db=os.getenv("DB_NAME_1")
db_user=os.getenv("DB_USER")
db_pass=os.getenv("DB_PASSWOrD")
DATABASE_URL = f"postgresql://{db_user}:{db_pass}@localhost/{db}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def initialize_database():
    Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    