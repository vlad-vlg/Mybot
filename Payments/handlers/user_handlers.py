from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, KeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

user_router = Router()


class Goods(CallbackData, prefix='goods'):
    name: str
    price: float


items = {
    'Шляпа': 19,99,
    'Сумка': 25,
    'Зонт': 49,99
}


def get_menu_items():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Шляпа',
        callback_data=Goods(
            name='Шляпа',
            price=19,99
        )
    )
    builder.button(
        text='Сумка',
        callback_data=Goods(
            name='Сумка',
            price=25
        )
    )
    builder.button(
        text='Зонт',
        callback_data=Goods(
            name='Зонт',
            price=49,99
        )
    )
    builder.adjust(1)
    menu_items_kbd = builder.as_markup()
    return menu_items_kbd


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.first_name:
        text = f'Привет, {message.from_user.first_name}!'
    else:
        text = 'Привет!'
    await message.answer(text)
    await message.answer(
        'Это задание к уроку 7.11 <b>"Прием платежей с помощью API"</b>\n\n'
        'Для начала выполнения наберите команду /items\n'
        'Для возврата в начальное меню наберите команду /cancel'
    )


@user_router.message(Command('cancel'))
async def cmd_cancel(message: Message):
    await message.answer(
        'Вернулись в начало'
    )


@user_router.message(Command('items'))
async def cmd_items(message: Message):
    menu_items_kbd = get_menu_items()
    await message.answer(
        'Выберите товар',
        reply_markup=menu_items_kbd
    )


@user_router.callback_query(Goods.filter())
async def select_item(call: CallbackQuery, callback_data: Goods):
    name = callback_data.name
    price = callback_data.price
    # button_item = call.message.reply_markup.inline_keyboard[int(item_id)-1]
    # item = button_item[0].text
    await call.message.answer(
        text='Вы Выбрали: \n'
        f'<b>{name}</b>\n'
        # f'ID товара - {item_id}\n'
        # f'Категория  - {category}\n\n',
        # reply_markup=get_menu_task_3()
        f'Теперь выберите валюту платежа - наберите команду /currency'
    )
    await call.answer(text='Отличный выбор!')
