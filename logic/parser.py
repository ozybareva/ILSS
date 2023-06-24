import re
from logic.rules import DATE_RULE, SCHEDULE_RULE, COMMENTS_RULE

DAYS = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']


class Parser:

    def get_schedule(self, text):
        schedule = re.search(rf'{SCHEDULE_RULE}', text)
        if schedule:
            return schedule.group(2)

    def parse_tasks(self, schedule):
        for i in range(len(DAYS)):
            if DAYS[i] != 'воскресенье':
                info = re.search(rf'({DATE_RULE})(, {DAYS[i]})((.|\n)+)({DATE_RULE}, {DAYS[i + 1]})', schedule)
            else:
                info = re.search(rf'({DATE_RULE})(, {DAYS[i]})((.|\n)+)', schedule)
            comment = info.group(5)
            day_of_week = DAYS[i]
            date = info.group(2, 3)
            print(date, comment, day_of_week)

    def get_comments(self, text):
        return re.search(rf'{COMMENTS_RULE}', text).group()
