import asyncio
import logging
import aiomysql
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from infrastructure.payments.api import NowPaymentsAPI
from middlewares.nowpayments import PaymentsMiddleware
from middlewares.database import DatabaseMiddleware
from handlers.payments import payments_router
from handlers.user_handlers import user_router
from handlers.other_handlers import other_router
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
    nowpayments = NowPaymentsAPI(config.payments_api_key)
    aiomysql_pool = await aiomysql.create_pool(
        host=config.db.host,
        port=config.db.port,
        user=config.db.user,
        password=config.db.password,
        db=config.db.database
    )
    dp = Dispatcher(storage=storage)
    dp.include_routers(user_router, payments_router, other_router)
#    dp.include_router(payments_router)
#    dp.include_router(other_router)
    dp.message.middleware(PaymentsMiddleware(nowpayments))
    dp.callback_query.middleware(PaymentsMiddleware(nowpayments))
    dp.message.middleware(DatabaseMiddleware(aiomysql_pool))
    dp.callback_query.middleware(DatabaseMiddleware(aiomysql_pool))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
