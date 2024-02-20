# import requests
import  aiohttp
import  asyncio


def make_send_message_url(token, chat_id, text):
    base_url = 'https://api.telegram.org'
    return f'{base_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}'


def get_updates_url(token, offset=None):
    base_url = 'https://api.telegram.org'
    return f'{base_url}/bot{token}/getUpdates?offset={offset}'


async def answer_to_message(session, token, update):
    chat_id = update['message']['chat']['id']
    url = make_send_message_url(
        token, chat_id, 'Наш ответ!'
    )
    async with session.get(url) as response:
        result = await response.json()
        print(result)


async def main():
    token = '6101955433:AAFIqsV8NRXr6S05Uajr265hJUUbmv-jrfg'
    offset = -1
#    url = make_send_message_url(
#        '6101955433:AAFIqsV8NRXr6S05Uajr265hJUUbmv-jrfg',
#        1456359683,
#        'Привет!'
#    )
    async with aiohttp.ClientSession() as session:
        while True:
            url = get_updates_url(token, offset=offset)
            async with session.get(url) as response:
                result = await response.json()
#               user_first_name = result['result']['chat']['first_name']
#               print(f'{user_first_name} отправил сообщение')
                for update in result['result']:
                    await answer_to_message(session, token, update)
                    offset = update['update_id'] + 1
            await asyncio.sleep(1)

#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())

# response = requests.get(url)
# result = response.json()
# print(result)
# first_name = result['result']['from']['first_name']
# print(first_name)
