import json
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from Database.infrastructure.database.requests import create_new_order

user_router = Router()


class Goods(CallbackData, prefix='goods'):
    name: str
    price: float


class Payments(CallbackData, prefix='payment'):
    my_item_name: str
    my_item_price: float
    my_currency: str
    order_id: int


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
            text=f'{name} - ${price}',
            callback_data=Goods(
                name=name,
                price=price
            )
        )
    builder.adjust(1)
    menu_items_kbd = builder.as_markup()
    return menu_items_kbd


def get_menu_order():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Подтвердите заказ',
        callback_data='order'
    )
    builder.adjust(1)
    menu_order_kbd = builder.as_markup()
    return menu_order_kbd


def get_menu_currencies(item, order_id):
    builder = InlineKeyboardBuilder()
    for i in range(12):
        builder.button(
            text=my_currencies[i],
            callback_data=Payments(
                my_item_name=item['name'],
                my_item_price=item['price'],
                my_currency=my_currencies[i],
                order_id=order_id
            )
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
        'Это задание к уроку 7.12 <b>"Работа с базой данных в боте"</b>\n\n'
        'Для выбора товара наберите команду /items\n'
        'Для просмотра состояния Вашего счета наберите команду /get_balance\n'
        'Для возврата в начальное меню наберите команду /cancel'
    )


@user_router.message(Command('cancel'))
async def cmd_cancel(message: Message):
    await message.answer(
        'Вернулись в начало\n'
        'Наберите команду /start'
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

    menu_order_kbd = get_menu_order()
    await call.message.answer(
        text='Вы Выбрали: \n\n'
             f'Наименование: <b>{name}</b>\n'
             f'Цена товара: <b>${price}</b>',
        reply_markup=menu_order_kbd
    )
    print(my_item)
    await call.answer(text='Отличный выбор!')


@user_router.callback_query(F.data == 'order')
async def cmd_create_order(call: CallbackQuery, db_connection):
    order_info = my_item
    amount = my_item['price']

    order_id = await create_new_order(db_connection, call.from_user.id, amount, json.dumps(order_info))

    menu_currencies_kbd = get_menu_currencies(my_item, order_id)
    await call.message.answer(
        f'Создан заказ с ID {order_id}.\n\n'
        'Для оплаты заказа выберите валюту платежа',
        reply_markup=menu_currencies_kbd
    )
