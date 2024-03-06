import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from FSM_medicine.tgbot.Handlers.form import form_router
from FSM_medicine.tgbot.config import load_config, Config


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    config: Config = load_config()
    storage = MemoryStorage()
    bot = Bot(token=config.tgbot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
