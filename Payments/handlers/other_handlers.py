from aiogram import Router
from aiogram.types import Message


router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message):
    await message.answer(
        'Моя твоя не понимать...\n\n'
        'Для отмены отправьте команду /cancel\n'
        'Для возврата в начало работы отправьте команду /start'
    )
