from sqlalchemy import select
from persistance.postgres_connection import PostgresConnector
from persistance.models import Schedule, TaskModel


class Repository:
    def __init__(self, postgres: PostgresConnector):
        self.postgres_session = postgres.get_session()

    def bulk_write_to_db(self, models):
        self.postgres_session.add_all(models)
        self.postgres_session.commit()

    def write_to_db(self, model):
        self.postgres_session.add(model)
        self.postgres_session.commit()

    async def get_schedule(self):
        stmt = select(Schedule.schedule).filter()
        return self.postgres_session.scalar(stmt)

    async def get_task_by_date(self, date):
        stmt = select(TaskModel.task).filter()
        return self.postgres_session.scalar(stmt)
