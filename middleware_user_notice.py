import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware, Bot, Dispatcher, F
from aiogram.types import TelegramObject, Message, User
from config_reader import config


class UserNoticeMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
            user: User = data['event_from_user'].first_name
            await handler(event, data)
            print(event)
            await event.answer(f'{user}, Ваш запрос выполнен успешно!')


async def notice_user(message: Message):
    await message.answer_location(55.753544, 37.621202)


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.message.middleware(UserNoticeMiddleware())
    dp.message.register(notice_user, F.text)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
