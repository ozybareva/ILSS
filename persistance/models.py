from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
     pass


class ScheduleModel(Base):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    week = Column('week', Integer)
    year = Column('year', Integer)
    schedule = Column('schedule', String, nullable=True)
    train_results = Column('train_results', String, nullable=True)
    comment = Column('comment', String, nullable=True)


class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    date = Column('date', Date)
    day_of_week = Column('day_of_week', String)
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

