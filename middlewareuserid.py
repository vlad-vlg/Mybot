import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware, Bot, Dispatcher, F
from aiogram.types import TelegramObject, Message
from config_reader import config


class UserIdMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user = data.get('event_from_user')
        data['user_id'] = user.id
        return await handler(event, data)


async def show_user_id(message: Message, user_id):
    user = user_id
    await message.answer(f'User ID: {user}')


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.message.outer_middleware(UserIdMiddleware())
    dp.message.register(show_user_id, F.text)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
