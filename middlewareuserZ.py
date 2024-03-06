import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware, Bot, Dispatcher, F
from aiogram.types import TelegramObject, Message, User
from config_reader import config


class UserZMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        age = event.text
        print(age)
        print(type(age))
        if age.isdigit() and int(age) >= 18:
            if int(age) > 100:
                await event.answer('О, да Вы долгожитель!')
                return await handler(event, data)
            else:
                return await handler(event, data)
        await event.answer(
            'Вы еще слишком молоды!\n'
            'Обратитесь после достижения совершеннолетия'
        )
        user: User = data['event_from_user']
        print(user)
        user_name = user.first_name.lower()
        if not user_name.startswith('z') and not user_name.__contains__('z'):
            return await handler(event, data)
        print(f'Ваше имя {user.first_name} не проходит!')


async def show_user_id(message: Message):
    await message.answer(f'Вы прошли наш Z-фильтр!')


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.message.outer_middleware(UserZMiddleware())
    dp.message.register(show_user_id, F.text)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
