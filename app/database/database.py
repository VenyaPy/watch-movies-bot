from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy

engine = create_engine('sqlite:////app/app/database/kinobot.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = sqlalchemy.orm.declarative_base()
