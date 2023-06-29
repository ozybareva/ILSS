import re
from datetime import datetime
from logic.rules import DATE_RULE, SCHEDULE_RULE, COMMENTS_RULE, TRAIN_RESULTS_RULE
from persistance.models import TaskModel

DAYS = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']


class Parser:

    def get_schedule(self, text):
        schedule = SCHEDULE_RULE.search(text)
        if schedule:
            return schedule.group(2)

    def get_train_results(self, text):
        train_results = TRAIN_RESULTS_RULE.search(text)
        if train_results:
            return train_results.group(2)

    def get_comments(self, text):
        comments = COMMENTS_RULE.search(text)
        if comments:
            return comments.group()

    def get_week(self, msg_date):
        week = msg_date.isocalendar()[1]
        return week

    def get_year(self, msg_date):
        year = msg_date.year
        return year


    def parse_tasks(self, schedule, msg_date):
        tasks = []
        if not schedule:
            return
        for i in range(len(DAYS)):
            if DAYS[i] != 'воскресенье':
                info = re.search(rf'({DATE_RULE})(, {DAYS[i]})((.|\n)+)({DATE_RULE}, {DAYS[i + 1]})', schedule)
            else:
                info = re.search(rf'({DATE_RULE})(, {DAYS[i]})((.|\n)+)', schedule)
            if info:
                task = info.group(5)
                day_of_week = DAYS[i]
                week = msg_date.isocalendar()[1]
                date = self.postprocess_date(info.group(2, 3), msg_date)
                new_task = TaskModel(date=date, day_of_week=day_of_week, week=week, task=task)
                tasks.append(new_task)
        return tasks

    def postprocess_date(self, task_date, msg_date):
        day = int(task_date[0])
        month_name = task_date[1]

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
        month_number = month.get(month_name)
        year = msg_date.year
        return datetime(day=day, month=month_number, year=year).date()
