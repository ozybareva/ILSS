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
        self.mail_client.login()
        message_dict = self.mail_client.get_messages_in_folder('ILSS')
        schedule_model_list = []
        for msg_date, msg_text in message_dict.items():
            task_models_list, schedule_model = self.parse_message(msg_text, msg_date)
            schedule_model_list.append(schedule_model)

            self.repository.bulk_write_to_db(task_models_list)
        self.repository.bulk_write_to_db(schedule_model_list)

    async def process_unread_messages(self):
        self.mail_client.login()
        new_message_dict = self.mail_client.get_new_messages_in_folder('ILSS')
        schedule_model_list = []
        for msg_date, msg_text in new_message_dict.items():
            task_model_list, schedule_model = self.parse_message(msg_text, msg_date)
            schedule_model_list.append(schedule_model)

            msg = await self.bot.send_message(chat_id=self.settings.chat_id, message=schedule_model.schedule)
            await self.bot.bot.pin_chat_message(chat_id=self.settings.chat_id, message_id=msg.message_id)
            self.repository.bulk_write_to_db(task_model_list)
        self.repository.bulk_write_to_db(schedule_model_list)

    def parse_message(self, msg_text: str, msg_date):
        try:
            schedule_model = self.parser.get_schedule_model(msg_text, msg_date)
            task_models = self.parser.parse_tasks(schedule_model.schedule, msg_date)
            return task_models, task_models
        except Exception as ex:
            logging.warning(f'Parsing error {ex}')
            return None, None

