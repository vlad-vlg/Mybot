# import requests
import aiohttp
import asyncio

base_url = 'https://api.telegram.org'
photo = 'https://experience-ireland.s3.amazonaws.com/thumbs2/b3d52580-d200-11e8-9b53-02b782d69cda.384x289.jpg'
caption = 'Hello, Universe!'
emoji = '🏀&reply_markup={"inline_keyboard": [[{"text": "🎳", "callback_data": "string"}]]}'
lat = 55.74945068
lon = 37.54282379

def make_send_message_url(token, chat_id, text):
    return f'{base_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}'

def make_send_photo_url(token, chat_id, photo, caption):
    return f'{base_url}/bot{token}/sendPhoto?chat_id={chat_id}&photo={photo}&caption={caption}'

def make_send_dice_url(token, chat_id, emo):
    return f'{base_url}/bot{token}/sendDice?chat_id={chat_id}&emoji={emo}'

def make_send_location_url(token, chat_id, latitude, longitude):
    return f'{base_url}/bot{token}/sendLocation?chat_id={chat_id}&latitude={latitude}&longitude={longitude}'

def get_updates_url(token, offset=None):
    return f'{base_url}/bot{token}/getUpdates?offset={offset}'

async def answer_to_message(session, token, update):
    chat_id = update['message']['chat']['id']
    message = update['message']['text']
    if message == '1':
        url = make_send_photo_url(token, chat_id, photo, caption)
    elif message == '2':
        url = make_send_dice_url(token, chat_id, emoji)
    elif message == '3':
        url = make_send_location_url(token, chat_id, lat, lon)
    else:
        url = make_send_message_url(token, chat_id, 'Наш ответ!')
    async with session.get(url) as response:
        result = await response.json()
        print(result)

async def main():
    token = '6101955433:AAFIqsV8NRXr6S05Uajr265hJUUbmv-jrfg'
    offset = -1
    async with aiohttp.ClientSession() as session:
        while True:
            url = get_updates_url(token, offset=offset)
            async with session.get(url) as response:
                result = await response.json()
                # user_first_name = result['result']['chat']['first_name']
                # print(f'{user_first_name} отправил сообщение')
                for update in result['result']:
                    await answer_to_message(session, token, update)
                    offset = update['update_id'] + 1
            await asyncio.sleep(5)

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())

# response = requests.get(url)
# result = response.json()
# print(result)
# first_name = result['result']['from']['first_name']
# print(first_name)
