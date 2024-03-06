import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import profile_form
from config.config import load_config, Config


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    config: Config = load_config()
    storage = MemoryStorage()
    bot = Bot(token=config.tgbot.token,
              default=DefaultBotProperties(parse_mode='html')
    )
    dp = Dispatcher(storage=storage)
    dp.include_router(profile_form.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
