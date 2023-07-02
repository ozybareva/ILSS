import re
from datetime import datetime
from logic.rules import DATE_RULE, SCHEDULE_RULE, COMMENTS_RULE, TRAIN_RESULTS_RULE
from persistance.models import TaskModel, ScheduleModel

DAYS = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']


class MessageParser:

    def get_schedule(self, text: str):
        schedule = SCHEDULE_RULE.search(text)
        if schedule:
            return schedule.group(2)

    def get_train_results(self, text: str):
        train_results = TRAIN_RESULTS_RULE.search(text)
        if train_results:
            return train_results.group(2)

    def get_comments(self, text: str):
        comments = COMMENTS_RULE.search(text)
        if comments:
            return comments.group()

    def get_week(self, msg_date: datetime):
        week = msg_date.isocalendar()[1]
        return week

    def get_year(self, msg_date: datetime):
        year = msg_date.year
        return year

    def get_schedule_model(self, msg_text: str, msg_date: datetime) -> ScheduleModel:
        schedule = self.get_schedule(msg_text)
        comment = self.get_comments(msg_text)
        train_results = self.get_train_results(msg_text)
        week = self.get_week(msg_date)
        year = self.get_year(msg_date)
        schedule_model = ScheduleModel(year=year, week=week, schedule=schedule, comment=comment,
                                       train_results=train_results)
        return schedule_model

    def parse_tasks(self, schedule: str, msg_date: datetime) -> list[TaskModel] | None:
        tasks = []
        if not schedule:
            return tasks
        for i in range(len(DAYS)):
            if DAYS[i] != 'воскресенье':
                info = re.search(rf'({DATE_RULE})(, {DAYS[i]})((.|\n)+)({DATE_RULE}, {DAYS[i + 1]})', schedule)
            else:
                info = re.search(rf'({DATE_RULE})(, {DAYS[i]})((.|\n)+)', schedule)
            if info:
                task = info.group(5)
                day_of_week = DAYS[i]
                task_week = self.get_week(msg_date)
                task_date = self.postprocess_date(info.group(2), info.group(3), msg_date)
                new_task = TaskModel(date=task_date, day_of_week=day_of_week, week=task_week, task=task)
                tasks.append(new_task)
        return tasks

    def postprocess_date(self, task_day, task_month, msg_date):
        month = {
            "января": 1,
            "февраля": 2,
            "марта": 3,
            "апреля": 4,
            "мая": 5,
            "июня": 6,
            "июля": 7,
            "августа": 8,
            "сентября": 9,
            "октября": 10,
            "ноября": 11,
            "декабря": 12
        }
        month_number = month.get(task_month)
        year = msg_date.year
        return datetime(day=int(task_day), month=month_number, year=year).date()

    def define_task_year(self, msg_date: datetime):
        #TODO: граничное условие для определения года таски
        pass
