from injector import provider, singleton, Module

from application.routers import MessageRouter
from clients.mail_client import MailClient
from logic.message_parser import MessageParser
from logic.bot.tg_bot import ILSSBot
from logic.message_processor import MessageProcessor
from persistance.postgres_connection import PostgresConnector
from persistance.repository import Repository
from settings import Settings


class Container(Module):

    @provider
    @singleton
    def provide_settings(self) -> Settings:
        return Settings()

    @provider
    @singleton
    def provide_postgres_connection(self, settings: Settings) -> PostgresConnector:
        return PostgresConnector(settings)

    @provider
    @singleton
    def provide_repository(self, postgres: PostgresConnector) -> Repository:
        return Repository(postgres)

    @provider
    @singleton
    def provide_mail_client(self, settings: Settings) -> MailClient:
        return MailClient(settings)

    @provider
    @singleton
    def provide_tg_bot(self, settings: Settings, repository: Repository) -> ILSSBot:
        return ILSSBot(settings, repository)

    @provider
    @singleton
    def provide_parser(self) -> MessageParser:
        return MessageParser()

    @provider
    @singleton
    def provide_message_processor(
            self,
            settings: Settings,
            mail_client: MailClient,
            repository: Repository,
            parser: MessageParser,
            ilss_bot: ILSSBot
    ) -> MessageProcessor:
        return MessageProcessor(settings, mail_client, repository, parser, ilss_bot)

    @provider
    @singleton
    def provide_message_router(
            self,
            message_processor: MessageProcessor
    ) -> MessageRouter:
        return MessageRouter(message_processor)
