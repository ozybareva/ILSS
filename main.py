from clients.mail_client import MailClient
from logic.parser import Parser
from settings import Settings


def main():
    settings = Settings()
    mail_client = MailClient(settings)
    parser = Parser()

    mail_client.login()
    message_list = mail_client.read_messages_in_folder('ILSS')
    for message in message_list:
        schedule = parser.get_schedule(message)
        task_info = parser.parse_tasks(schedule)
        comments = parser.get_comments(message)

main()