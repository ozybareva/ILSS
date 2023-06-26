import re
from datetime import datetime
from logic.rules import DATE_RULE, SCHEDULE_RULE, COMMENTS_RULE
from persistance.models import TaskModel

DAYS = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']


class Parser:

    def get_schedule(self, text):
        schedule = SCHEDULE_RULE.search(text)
        if schedule:
            return schedule.group(2)

    def parse_tasks(self, schedule, msg_date):
        tasks = []
        if not schedule:
            return
        for i in range(len(DAYS)):
            if DAYS[i] != 'воскресенье':
                info = re.search(rf'({DATE_RULE})(, {DAYS[i]})((.|\n)+)({DATE_RULE}, {DAYS[i + 1]})', schedule)
            else:
                info = re.search(rf'({DATE_RULE})(, {DAYS[i]})((.|\n)+)', schedule)
            task = info.group(5)
            day_of_week = DAYS[i]
            week = msg_date.isocalendar()[1]
            date = self.postprocess_date(info.group(2, 3), msg_date)
            new_task = TaskModel(date=date, day_of_week=day_of_week, week=week,
                                 task=task)
            tasks.append(new_task)
        return tasks

    def get_comments(self, text):
        return COMMENTS_RULE.search(text).group()

    def postprocess_date(self, date, msg_date):
        day = int(date[0])
        month_name = date[1]

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
