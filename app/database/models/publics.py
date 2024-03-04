from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy import Column, Integer, String, DateTime, BIGINT
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = sqlalchemy.orm.declarative_base()

class Publics(Base):
    __tablename__ = 'publics'

    id = Column(Integer, primary_key=True)
    id_pub = Column(BIGINT)
    url_pub = Column(String)


engine = create_engine('sqlite:////home/venya/Документы/python/KINOBT/app/database/database.db', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()