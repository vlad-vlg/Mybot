from environs import Env
from dataclasses import dataclass

from typing_extensions import Union


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tgbot: TgBot


def load_config(path: Union[str, None] = '.env') -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tgbot=TgBot(
            token=env.str('BOT_TOKEN')
        )
    )
