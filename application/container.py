from injector import provider, singleton, Module
from clients.mail_client import MailClient
from logic.parser import Parser
from logic.bot.tg_bot import ILSSBot
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
    def provide_parser(self) -> Parser:
        return Parser()
