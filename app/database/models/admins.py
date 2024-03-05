from sqlalchemy import create_engine, Column, Integer, String, Date, BIGINT
from sqlalchemy import Column, Integer, String, DateTime
import sqlalchemy
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = sqlalchemy.orm.declarative_base()


class Admins(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    user_id = Column(BIGINT)


# Создание экземпляра движка SQLite
engine = create_engine('sqlite:////home/venya/Документы/python/KINOBT/app/database/database.db', echo=True)

# Создание всех определенных таблиц
Base.metadata.create_all(engine)

# Создание сессии для выполнения операций с базой данных
Session = sessionmaker(bind=engine)
session = Session()