from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

user_router = Router()


class Goods(CallbackData, prefix='goods'):
    name: str
    price: float


items = {
    'Шляпа': 19.99,
    'Сумка': 25,
    'Зонт': 49.99
}
my_currencies = ['btc', 'eth', 'xmr', 'zec', 'xvg', 'ada', 'ltc', 'bch', 'ark', 'waves', 'bnb', 'apt']
my_item = {}


def get_menu_items(x):
    builder = InlineKeyboardBuilder()
    for key in x:
        name = key
        price = x[key]
        builder.button(
            text=name,
            callback_data=Goods(
                name=name,
                price=price,
                my_item=my_item
            )
        )
    builder.adjust(1)
    menu_items_kbd = builder.as_markup()
    return menu_items_kbd


def get_menu_currencies():
    builder = InlineKeyboardBuilder()

    for i in range(12):
        builder.button(
            text=my_currencies[i],
            callback_data=my_currencies[i]
        )
    builder.adjust(4)
    menu_currencies_kbd = builder.as_markup()
    return menu_currencies_kbd


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
    menu_items_kbd = get_menu_items(items)
    await message.answer(
        'Выберите товар',
        reply_markup=menu_items_kbd
    )


@user_router.callback_query(Goods.filter())
async def select_item(call: CallbackQuery, callback_data: Goods):
    name = callback_data.name
    price = callback_data.price
    my_item['name'] = name
    my_item['price'] = price
    await call.message.answer(
        text='Вы Выбрали: \n'
             f'Наименование: <b>{name}</b>\n'
             f'Цена товара: <b>${price}</b>\n'
             f'Теперь выберите валюту платежа - наберите команду /currency'
    )
    print(my_item)
    await call.answer(text='Отличный выбор!')


@user_router.message(Command('currency'))
async def cmd_currency(message: Message):
    menu_currencies_kbd = get_menu_currencies()
    await message.answer(
        'Выберите валюту платежа',
        reply_markup=menu_currencies_kbd
    )
