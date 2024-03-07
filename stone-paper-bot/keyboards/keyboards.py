from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

button_yes = KeyboardButton(text='Давай!')
button_no = KeyboardButton(text='Не хочу!')
yes_no_kb_builder = ReplyKeyboardBuilder()
yes_no_kb_builder.row(button_yes, button_no, width=2)
yes_no_kb = yes_no_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)

button_1 = KeyboardButton(text='Камень 🗿')
button_2 = KeyboardButton(text='Ножницы ✂')
button_3 = KeyboardButton(text='Бумага 📜')
game_kb = ReplyKeyboardMarkup(
    keyboard=[[button_1, button_2, button_3]],
    resize_keyboard=True
)
