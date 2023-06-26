from clients.mail_client import MailClient
from logic.parser import Parser
from persistance.postgres_connection import PostgresConnector
from settings import Settings


def main():
    settings = Settings()
    mail_client = MailClient(settings)
    postgres = PostgresConnector(settings)
    postgres.declare_base()
    session = postgres.create_session()
    parser = Parser()

    mail_client.login()
    message_dict = mail_client.read_messages_in_folder('ILSS')
    for date, msg_text in message_dict.items():
        schedule = parser.get_schedule(msg_text)
        tasks = parser.parse_tasks(schedule, date)
     #   comments = parser.get_comments(msg_text)

        session.add_all(tasks)
        session.commit()

main()