from environs import Env
from dataclasses import dataclass

from typing_extensions import Union


@dataclass
class DBConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tgbot: TgBot
    payments_api_key: str
    db: DBConfig


def load_config(path: Union[str, None] = '.env') -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tgbot=TgBot(
            token=env.str('BOT_TOKEN')
        ),
        payments_api_key=env.str('NOWPAYMENTS_API_KEY'),
        db=DBConfig(
            host=env.str('MYSQL_HOST'),
            port=env.int('MYSQL_PORT'),
            user=env.str('MYSQL_USER'),
            password=env.str('MYSQL_ROOT_PASSWORD'),
            database=env.str('MYSQL_DATABASE')
        )
    )
