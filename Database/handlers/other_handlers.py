from aiogram import Router
from aiogram.types import Message


other_router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@other_router.message()
async def send_answer(message: Message):
    await message.answer(
        'Моя твоя не понимать...\n\n'
        'Для отмены отправьте команду /cancel\n'
        'Для возврата в начало работы отправьте команду /start'
    )
