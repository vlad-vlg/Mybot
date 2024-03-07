from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.keyboards import game_kb, yes_no_kb
from services.services import get_bot_choice, get_winner, LEXICON_RU

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.first_name:
        text = f'Привет, {message.from_user.first_name}!'
    else:
        text = 'Привет!'
    await message.answer(text)
    await message.answer(
        'Давай с тобой сыграем в игру '
        '"Камень, ножницы, бумага"?\n\n'
        'Если ты, вдруг, забыл правила, '
        'команда /help тебе поможет!\n\n'
        '<b>Играем?</b>',
        reply_markup=yes_no_kb
    )


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        'Это очень простая игра. Мы одновременно должны '
        'сделать выбор одного из трех предметов: камень, '
        'ножницы или бумага.\n\nЕсли наш выбор '
        'совпадает - ничья, а в остальных случаях камень '
        'побеждает ножницы, ножницы побеждают бумагу, '
        'а бумага побеждает камень.\n\n<b>Играем?</b>',
        reply_markup=yes_no_kb
    )


@router.message(Command('delmenu'))
async def cmd_main_menu_delete(message: Message, bot: Bot):
    await bot.delete_my_commands()
    await message.answer('Кнопка "Menu" удалена',
                         reply_markup=ReplyKeyboardRemove()
                         )

@router.message(F.text == 'Давай!')
async def cmd_yes_answer(message: Message):
    await message.answer('Отлично! Делай свой выбор!',
                         reply_markup=game_kb
                         )


@router.message(F.text == 'Не хочу!')
async def cmd_no_answer(message: Message):
    await message.answer(
        'Жаль...\nЕсли захочешь сыграть, '
        'просто разверни клавиатуру и нажми кнопку "Давай!"'
    )


@router.message(F.text.in_(['Камень 🗿',
                            'Ножницы ✂',
                            'Бумага 📜']))
async def cmd_game_button(message: Message):
    bot_choice = get_bot_choice()
    await message.answer(
        'Мой выбор '
        f'- {LEXICON_RU[bot_choice]}')
    winner = get_winner(message.text, bot_choice)
    await message.answer(winner,
                         reply_markup=yes_no_kb
                         )
