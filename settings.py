from os.path import isfile
from pathlib import Path
from pydantic import BaseSettings

base_dir = Path(__file__).parent.absolute()
print(base_dir)


class Settings(BaseSettings):
    mail_host: str
    mail_user: str
    mail_password: str

    class Config:
        config_file_name = f'{base_dir}/.env'
        if isfile(config_file_name):
            env_file = config_file_name
