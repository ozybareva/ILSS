import logging
from injector import Injector

from clients.mail_client import MailClient
from logic.parser import Parser
from logic.bot.tg_bot import ILSSBot
from persistance.repository import Repository
from persistance.models import Schedule
from settings import Settings

injector = Injector()


class MessageProcessor:
    def __init__(self):
        self.settings = injector.get(Settings)
        self.mail_client = injector.get(MailClient)
        self.repository = injector.get(Repository)
        self.parser = injector.get(Parser)
        self.bot = injector.get(ILSSBot)

    async def process_all_messages(self):
        self.mail_client.login()
        message_dict = self.mail_client.get_messages_in_folder('ILSS')
        schedules = []
        for msg_date, msg_text in message_dict.items():
            tasks, schedule_model = self.parse_message(msg_date, msg_text)
            schedules.append(schedule_model)

            self.repository.bulk_write_to_db(tasks)
        self.repository.bulk_write_to_db(schedules)

    async def process_new_messages(self):
        self.mail_client.login()
        new_message_dict = self.mail_client.get_new_messages_in_folder('ILSS')
        schedules = []
        for msg_date, msg_text in new_message_dict.items():
            tasks, schedule_model = self.parse_message(msg_date, msg_text)
            schedules.append(schedule_model)

            await self.bot.send_message(chat_id=self.settings.chat_id, message=schedule_model.schedule)
            self.repository.bulk_write_to_db(tasks)
        self.repository.bulk_write_to_db(schedules)

    def parse_message(self, msg_date, msg_text):
        try:
            schedule = self.parser.get_schedule(msg_text)
            comment = self.parser.get_comments(msg_text)
            train_results = self.parser.get_train_results(msg_text)
            week = self.parser.get_week(msg_date)
            year = self.parser.get_year(msg_date)
            tasks = self.parser.parse_tasks(schedule, msg_date)
            schedule_model = Schedule(year=year, week=week, schedule=schedule, comment=comment, train_results=train_results)
            return tasks, schedule_model
        except Exception as ex:
            logging.warning(f'Parsing error {ex}')
            return None, None

