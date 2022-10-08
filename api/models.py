from database import Base
from sqlalchemy import Column, String, Integer, Float


class User(Base):
    __tablename__ = 'User'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    mail = Column('mail', String)
    age = Column('age', Integer)


class Weather(Base):
    __tablename__ = 'Weather'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    city = Column('city', String, index=True)
    date = Column('date', String)
    day = Column('day', String)
    description = Column('description', String)
    degree = Column('degree', Float)
