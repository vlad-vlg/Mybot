from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

router = Router()


class Goods(CallbackData, prefix='goods'):
    category: str
    item_id: int


def get_main_menu_keyboard():
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


def get_menu_task_1():
    builder = ReplyKeyboardBuilder()
    for i in range(1, 11):
        builder.add(KeyboardButton(text=f'Кнопка {i}'))
    builder.adjust(3, 2, 5)
    menu_task_1_kbd = builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Нажмите на кнопку для выбора варианта"
    )
    return menu_task_1_kbd


def get_menu_task_2():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(
            text='Простой текст'
        )
    )
    builder.row(
        KeyboardButton(
            text='Запрос контакта',
            request_contact=True
        )
    )
    builder.row(
        KeyboardButton(
            text='Запрос локации',
            request_location=True
        )
    )
    menu_task_2_kbd = builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Нажмите на кнопку для выбора варианта"
    )
    return menu_task_2_kbd


def get_menu_task_3():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Пила 🪚',
        callback_data=Goods(
            category='Инструменты',
            item_id=1
        )
    )
    builder.button(
        text='Стул 🪑',
        callback_data=Goods(
            category='Мебель',
            item_id=2
        )
    )
    builder.button(
        text='Чайник 🫖',
        callback_data=Goods(
            category='Посуда',
            item_id=3
        )
    )
    builder.adjust(1)
    menu_task_3_kbd = builder.as_markup()
    return menu_task_3_kbd


@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.first_name:
        text = f'Привет, {message.from_user.first_name}!'
    else:
        text = 'Привет!'
    await message.answer(text)
    await message.answer(
        'Это задание к уроку 7.9 <b>"Кнопки"</b>\n\n'
        'Для начала выполнения наберите команду /keyboards\n'
        'Для возврата в начальное меню наберите команду /cancel'
    )


@router.message(Command('keyboards'))
async def cmd_keyboards(message: Message):
    main_menu_kbd = get_main_menu_keyboard()
    await message.answer(
        'Это меню задания',
        reply_markup=main_menu_kbd
    )


@router.message(Command('cancel'))
async def cmd_cancel(message: Message):
    await message.answer(
        'Вернулись в начало',
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.text == 'Задание 1')
async def cmd_task_1(message: Message):
    menu_task_1_kbd = get_menu_task_1()
    await message.answer(
        'Это ответ на первое задание',
        reply_markup=menu_task_1_kbd
    )


@router.message(F.text.contains('Кнопка'))
async def cmd_return_main_menu(message: Message):
    await message.answer(
        'Возвращаемся в главное меню',
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.text == 'Задание 2')
async def cmd_task_2(message: Message):
    menu_task_2_kbd = get_menu_task_2()
    await message.answer(
        'Это ответ на второе задание',
        reply_markup=menu_task_2_kbd
    )


@router.message(F.text == 'Простой текст')
async def cmd_return_text(message: Message):
    await message.reply(
        'Возвращаемся в главное меню',
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.location)
async def cmd_return_location(message: Message):
    x = message.location.longitude
    y = message.location.latitude
    await message.answer(
        'Определили местоположение:\n\n'
        f'Долгота: <b>{x}</b>\n'
        f'Широта: <b>{y}</b>\n\n'
        'Возвращаемся в главное меню',
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.contact)
async def cmd_return_contact(message: Message):
    fist_name = message.contact.first_name
    last_name = message.contact.last_name
    user_id = message.contact.user_id
    phone_number = message.contact.phone_number
    await message.answer(
        'Определили контакты:\n\n'
        f'Имя: <b>{fist_name}</b>\n'
        f'Фамилия : <b>{last_name}</b>\n'
        f'ID пользователя : <b>{user_id}</b>\n'
        f'Телефон : <b>{phone_number}</b>\n\n'
        'Возвращаемся в главное меню',
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.text == 'Задание 3')
async def cmd_task_3(message: Message):
    menu_task_3_kbd = get_menu_task_3()
    await message.answer(
        'Это ответ на третье задание',
        reply_markup=menu_task_3_kbd
    )


@router.callback_query(Goods.filter())
async def select_item(call: CallbackQuery, callback_data: Goods):
    category = callback_data.category
    item_id = callback_data.item_id
    button_item = call.message.reply_markup.inline_keyboard[int(item_id)-1]
    item = button_item[0].text
    await call.message.answer(
        text='Вы Выбрали: \n'
        f'<b>{item}</b>\n'
        f'ID товара - {item_id}\n'
        f'Категория  - {category}\n\n',
        reply_markup=get_menu_task_3()
    )
    await call.answer(
        text='Отличный выбор!',
        show_alert=True
    )
