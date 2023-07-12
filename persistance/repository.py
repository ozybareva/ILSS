from datetime import date
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

    async def get_schedule_by_date(self, selected_date: date):
        stmt = select(ScheduleModel.schedule)\
            .filter(ScheduleModel.week == selected_date.isocalendar().week)\
            .filter(ScheduleModel.year == selected_date.year)
        return self.postgres_session.scalar(stmt)

    async def get_task_by_date(self, selected_date: date):
        stmt = select(TaskModel.task).filter(TaskModel.date == selected_date)
        return self.postgres_session.scalar(stmt)

    async def get_comment_by_date(self, selected_date: date):
        stmt = select(ScheduleModel.comment)\
            .filter(ScheduleModel.week == selected_date.isocalendar().week)\
            .filter(ScheduleModel.year == selected_date.year)
        return self.postgres_session.scalar(stmt)

    async def get_train_result_by_date(self, selected_date: date):
        week = selected_date.isocalendar().week
        year = selected_date.year if week >= 1 else selected_date.year - 1
        stmt = select(ScheduleModel.train_results)\
            .filter(ScheduleModel.week == week)\
            .filter(ScheduleModel.year == year)
        return self.postgres_session.scalar(stmt)
