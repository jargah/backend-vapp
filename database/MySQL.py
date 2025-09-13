from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import logging


connection_string = f'mysql+mysqlconnector://admin:d5758017c265@sandbox.cn7ga2jfbmbs.us-east-1.rds.amazonaws.com:3306/ven_app_api'

engine = create_engine(connection_string, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def rawDB():
    db = Session()
    try:
        yield db
    finally:
        db.close
