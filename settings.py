from os.path import isfile
from pathlib import Path
from pydantic import BaseSettings

base_dir = Path(__file__).parent.absolute()


class Settings(BaseSettings):
    mail_host: str
    mail_user: str
    mail_password: str

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    load_schedule_second: str = '00'
    load_schedule_minute: str = '53'
    load_schedule_hour: str = '11'
    load_schedule_day_of_week: str = 'mon'

    api_token: str
    chat_id: str

    @property
    def postgres_dsn(self) -> str:
        return f'postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'

    class Config:
        config_file_name = f'{base_dir}/.env'
        if isfile(config_file_name):
            env_file = config_file_name
