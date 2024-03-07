import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config.config import load_config, Config
from handlers import user_handlers, other_handlers
from keyboards.set_menu import set_main_menu

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Starting bot')
    config: Config = load_config()
    bot = Bot(token=config.tgbot.token,
              default=DefaultBotProperties(parse_mode='html')
              )
    dp = Dispatcher()
    await set_main_menu(bot)
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
