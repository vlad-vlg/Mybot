import asyncio
import random
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.enums import parse_mode
from aiogram.filters import Command
from aiogram.types import Update, Message
# from aiogram.enums.dice_emoji import DiceEmoji
from config_reader import config


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


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.message.register(start_command, Command(commands='start'))
    dp.message.register(product_command, Command(commands='product'))
    dp.message.register(dice_command, Command('dice'))
    dp.message.register(location_command, Command('location'))
    dp.message.register(quote_command, Command('quote'))

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
