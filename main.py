import asyncio
import random
import re
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, BaseFilter
from aiogram.types import Message
# from aiogram.enums.dice_emoji import DiceEmoji
from config_reader import config


async def check_is_admin(user_id: int):
    admins = [1, 2, 3]
    if user_id in admins:
        return admins


class IsAdmin(BaseFilter):
    async def __call__(self, message):
        admins_list = await check_is_admin(message.from_user.id)
        if admins_list:
            return {'admins_list': admins_list}


async def admin_only(message: Message, admins_list):
    await message.answer(f'Да, Вы админ!\nСписок администраторов: {admins_list}')


class FromTime(BaseFilter):
    async def __call__(self, *args, **kwargs):
        return None


async def start_command_referral(message: Message, bot: Bot, referral_match: re.Match):
    referral_id = referral_match.group(1)
    print(referral_id)
    await message.answer(f'Referral_ID: {referral_id}')


async def start_command(message: Message, bot: Bot):
    chat_id = message.chat.id
    text = '''
   Привет! Я бот, который отвечает на твои запросы!
Напиши /product, чтобы узнать про товар.
Напиши /dice, чтобы получить emoji.
Напиши /location, чтобы найти точку на карте.
Напиши /quote, чтобы прочитать цитату из "Игры престолов".
'''
    await bot.send_message(chat_id, text)


async def get_product(prodict_id):
    url = f'https://fakestoreapi.com/products/{prodict_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def product_command(message: Message, bot: Bot):
    chat_id = message.chat.id
    prod_id = random.randint(1, 20)
    product = await get_product(prod_id)
    title = product['title']
    price = product['price']
    image_url = product['image']
    description = product['description']
    rating = product['rating']['rate']
    count = product['rating']['count']
    rating = '❤' * int(rating) + f' ({count})'
    text = f'''
* Название: <b>{title}</b>
* Цена: <b>{price}</b> руб.
* Рейтинг: {rating}
* Описание:

<i>{description}</i>    
'''
    await bot.send_photo(chat_id, photo=image_url, caption=text, parse_mode='html')


async def dice_command(message: Message, bot: Bot):
    chat_id = message.chat.id
    # print(chat_id)
    emojis = ['🎲', '🎯', '🏀', '⚽', '🎳', '🎰']
    emo_id = random.randint(0, 5)
    await message.answer_dice(emoji=emojis[emo_id])


async def location_command(message: Message):
    latitude = 44.897171
    longitude = 37.313965
    await message.answer_location(latitude, longitude)


async def quote_command(message: Message):
    url = 'https://api.gameofthronesquotes.xyz/v1/random'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            quote = await response.json()
    sentence = quote['sentence']
    speaker = quote['character']['name']
    text = f'{speaker} сказал(а): \n\n\
- {sentence}'
    await message.answer(text)


async def help_command(message: Message):
    await message.answer('Вы нажали !HELP')


async def text_buy(message: Message):
    await message.answer('Вы решили купить чего-нибудь?')


async def anything(message: Message, text: re.Match):
    msg = text.group()
    await message.answer(f'Вы набрали не (/start | !start) \nВаш запрос - "{msg}"')


async def start_command_items(message: Message, bot: Bot, items_match: re.Match):
    item_id = items_match.group(1)
    quantity = items_match.group(2)
    # print(item_id, quantity)
    await message.answer(f'ID товара: {item_id}\nКоличество товара: {quantity}')


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.message.register(admin_only, IsAdmin())
    dp.message.register(start_command_referral,
                        CommandStart(deep_link=True),
                        F.text.regexp(r'.+ referral_(\d+)').as_('referral_match')
                        )
    dp.message.register(start_command_items,
                        CommandStart(deep_link=True),
                        F.text.regexp(r'.+ item_(\d+)_quantity_(\d+)').as_('items_match')
                        )
    dp.message.register(start_command, CommandStart())
    dp.message.register(product_command, Command(commands='product'))
    dp.message.register(dice_command, Command('dice'))
    dp.message.register(location_command, Command('location'))
    dp.message.register(quote_command, Command('quote'))
    dp.message.register(help_command, Command(commands='help', prefix='!', ignore_case=True))
    dp.message.register(text_buy, (F.text.lower() == 'купить') | (F.text == 'Приобрести товары'))
    dp.message.register(anything,
                        F.text != '/start',
                        F.text != '!start',
                        F.text.regexp(r'.+').as_('text')
                        )
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
