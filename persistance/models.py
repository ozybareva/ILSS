from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
     pass


class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    date = Column('date', Date)
    day_of_week = Column('type', String)
    week = Column('week', Integer)
    task = Column('task', String)


class PeopleModel(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    surname = Column('surname', String)
    second_surname = Column('second_surname', String, nullable=True)


class ResultModel(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    comment = Column('comment', String)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    person_id = Column(Integer, ForeignKey("people.id"))

