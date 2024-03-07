from sqlalchemy import create_engine, Column, Integer, String, Date, BIGINT
from sqlalchemy import Column, Integer, String, DateTime
import sqlalchemy
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from datetime import datetime


# Создание экземпляра движка SQLite
engine = create_engine('sqlite:////home/venya/Документы/python/KINOBOT/app/database/kinobot.db', echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = sqlalchemy.orm.declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    name = Column(String)
    email = Column(String, nullable=True)
    join_date = Column(DateTime, default=datetime.now)


class Publics(Base):
    __tablename__ = 'publics'

    id = Column(Integer, primary_key=True)
    id_pub = Column(BIGINT)
    url_pub = Column(String)


class Admins(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    user_id = Column(BIGINT)


Base.metadata.create_all(engine)