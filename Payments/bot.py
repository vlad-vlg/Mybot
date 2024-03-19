import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from infrastructure.payments.api import NowPaymentsAPI
from middlewares.nowpayments import PaymentsMiddleware
from handlers.payments import payments_router
from handlers.user_handlers import user_router
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
    dp = Dispatcher(storage=storage)
    dp.include_router(user_router)
    dp.include_router(payments_router)
    dp.message.middleware(PaymentsMiddleware(nowpayments))
    dp.callback_query.middleware(PaymentsMiddleware(nowpayments))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
