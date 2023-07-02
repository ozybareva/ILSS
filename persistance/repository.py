from sqlalchemy import select
from persistance.postgres_connection import PostgresConnector
from persistance.models import ScheduleModel, TaskModel


class Repository:
    def __init__(self, postgres: PostgresConnector):
        self.postgres_session = postgres.get_session()
        postgres.declare_base()

    def bulk_write_to_db(self, models):
        if models:
            self.postgres_session.add_all(models)
            self.postgres_session.commit()

    def write_to_db(self, model):
        self.postgres_session.add(model)
        self.postgres_session.commit()

    async def get_schedule_by_week(self, week):
        stmt = select(ScheduleModel.schedule).filter(ScheduleModel.week == week)
        return self.postgres_session.scalar(stmt)

    async def get_task_by_date(self, date):
        stmt = select(TaskModel.task).filter(TaskModel.date == date)
        return self.postgres_session.scalar(stmt)

    async def get_comment_by_week(self, week):
        stmt = select(ScheduleModel.comment).filter(ScheduleModel.week == week)
        return self.postgres_session.scalar(stmt)

    async def get_train_result_by_week(self, week):
        stmt = select(ScheduleModel.comment).filter(ScheduleModel.week - 1 == week)
        return self.postgres_session.scalar(stmt)
