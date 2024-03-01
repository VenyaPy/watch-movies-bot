from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy

engine = create_engine('sqlite:///D:\\python\\KINOBT\\app\\database\\database.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = sqlalchemy.orm.declarative_base()