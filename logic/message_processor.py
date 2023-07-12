import logging
from datetime import datetime
from injector import Injector

from clients.mail_client import MailClient
from logic.message_parser import MessageParser
from logic.bot.tg_bot import ILSSBot
from persistance.repository import Repository
from settings import Settings

injector = Injector()


class MessageProcessor:
    def __init__(self, settings: Settings, mail_client: MailClient, repository: Repository, parser: MessageParser, ilss_bot: ILSSBot):
        self.settings = settings
        self.mail_client = mail_client
        self.repository = repository
        self.parser = parser
        self.bot = ilss_bot

    async def process_all_messages(self):
        logging.info('Start process all messages history')
        self.mail_client.login()
        message_dict = self.mail_client.get_messages_in_folder('ILSS')
        schedule_model_list = []
        for msg_date, msg_text in message_dict.items():
            task_models_list, schedule_model = self.parse_message(msg_text, msg_date)
            if schedule_model:
                schedule_model_list.append(schedule_model)
                self.repository.bulk_write_to_db(task_models_list)
        self.repository.bulk_write_to_db(schedule_model_list)

    async def process_unread_messages(self):
        logging.info('Start process unread messages')
        self.mail_client.login()
        new_message_dict = self.mail_client.get_new_messages_in_folder('ILSS')
        schedule_model_list = []
        for msg_date, msg_text in new_message_dict.items():
            task_model_list, schedule_model = self.parse_message(msg_text, msg_date)
            if schedule_model:
                schedule_model_list.append(schedule_model)
                msg = await self.bot.send_message(message=schedule_model.schedule)
                await self.bot.unpin_messages()
                await self.bot.pin_message(message_id=msg.message_id)
                self.repository.bulk_write_to_db(task_model_list)
        self.repository.bulk_write_to_db(schedule_model_list)

    def parse_message(self, msg_text: str, msg_date: datetime):
        schedule_model = self.parser.get_schedule_model(msg_text, msg_date)
        if schedule_model:
            task_models = self.parser.parse_tasks(schedule_model.schedule, msg_date)
            return task_models, schedule_model
        else:
            return None, None

