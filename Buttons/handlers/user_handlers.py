from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()


def main_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    for i in range(1, 4):
        builder.add(KeyboardButton(text=f'Задание {i}'))
    builder.adjust(3)
    main_menu_kbd = builder.as_markup(
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Нажмите на кнопку для выбора варианта"
    )
    return main_menu_kbd


def menu_task_1():
    builder = ReplyKeyboardBuilder()
    for i in range(1, 11):
        builder.add(KeyboardButton(text=f'Кнопка {i}'))
    builder.adjust(3, 2, 5)
    menu_task_1_kbd = builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Нажмите на кнопку для выбора варианта"
    )
    return menu_task_1_kbd


def menu_task_2():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text='Простой текст'))
    builder.row(KeyboardButton(text='Запрос контакта',
                               request_contact=True)
                )
    builder.row(KeyboardButton(text='Запрос локации',
                               request_location=True)
                )
    menu_task_2_kbd = builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Нажмите на кнопку для выбора варианта"
    )
    return menu_task_2_kbd


@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.first_name:
        text = f'Привет, {message.from_user.first_name}!'
    else:
        text = 'Привет!'
    await message.answer(text)
    await message.answer(
        'Это задание у уроку 7.9 <b>"Кнопки"</b>\n\n'
        'Для начала выполнения набери команду /keyboards',
    )


@router.message(Command('keyboards'))
async def cmd_keyboards(message: Message):
    main_menu_kbd = main_menu_keyboard()
    await message.answer(
        'Это меню задания',
        reply_markup=main_menu_kbd
    )


@router.message(F.text == 'Задание 1')
async def cmd_task_1(message: Message):
    menu_task_1_kbd = menu_task_1()
    await message.answer('Это ответ на первое задание',
                         reply_markup=menu_task_1_kbd
                         )


@router.message(F.text.contains('Кнопка'))
async def cmd_return_main_menu(message: Message):
    await message.answer('Возвращаемся в главное меню',
                         reply_markup=main_menu_keyboard()
                         )


@router.message(F.text == 'Задание 2')
async def cmd_task_2(message: Message):
    menu_task_2_kbd = menu_task_2()
    await message.answer('Это ответ на второе задание',
                         reply_markup=menu_task_2_kbd
                         )


@router.message(F.text == 'Простой текст')
async def cmd_return_text(message: Message):
    await message.reply('Возвращаемся в главное меню',
                        reply_markup=main_menu_keyboard()
                        )


@router.message(F.location)
async def cmd_return_location(message: Message):
    x = message.location.longitude
    y = message.location.latitude
    await message.answer('Определили местоположение:\n\n'
                         f'Долгота: <b>{x}</b>\n'
                         f'Широта: <b>{y}</b>\n\n'
                         'Возвращаемся в главное меню',
                         reply_markup=main_menu_keyboard()
                         )


@router.message(F.contact)
async def cmd_return_location(message: Message):
    fist_name = message.contact.first_name
    last_name = message.contact.last_name
    user_id = message.contact.user_id
    phone_number = message.contact.phone_number
    await message.answer('Определили контакты:\n\n'
                         f'Имя: <b>{fist_name}</b>\n'
                         f'Фамилия : <b>{last_name}</b>\n'
                         f'ID пользователя : <b>{user_id}</b>\n'
                         f'Телефон : <b>{phone_number}</b>\n\n'
                         'Возвращаемся в главное меню',
                         reply_markup=main_menu_keyboard()
                         )
