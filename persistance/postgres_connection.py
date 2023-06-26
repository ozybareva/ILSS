from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from persistance.models import Base

from settings import Settings


class PostgresConnector:
    def __init__(self, settings: Settings):
        self.postgres_dsn = settings.postgres_dsn
        self.connection = None

    def get_connection(self):
        if not self.connection:
            self.connection = create_engine(self.postgres_dsn)
        return self.connection

    @property
    def declare_base(self):
        engine = self.get_connection()
        Base.metadata.create_all(engine)
        return Base

    def create_session(self):
        engine = self.get_connection()
        Session = sessionmaker(bind=engine)
        return Session()
