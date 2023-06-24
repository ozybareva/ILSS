from pydantic import BaseModel
from datetime import date
from enum import Enum


class TaskType(Enum):
    INTERVAL = 'interval'
    LONG = 'long'
    POWER = 'power'
    TEMPO = 'tempo'


class TaskModel(BaseModel):
    type: str
    date: date
    day_of_week: str
    week: int
    task: str


class ResultModel(BaseModel):
    task_id: str
    person_id: str
    comment: str
