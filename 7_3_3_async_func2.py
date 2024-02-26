import aiohttp
import asyncio


url_1 = 'https://api.gameofthronesquotes.xyz/v1/random'
url_2 = 'https://lucifer-quotes.vercel.app/api/quotes'
url_3 = 'https://strangerthings-quotes.vercel.app/api/quotes'


async def get_quote(url, session):
    colours = {
        url_1: '\33[33m',
        url_2: '\33[36m',
        url_3: '\33[31m',
    }
    url_num = {
        url_1: '1',
        url_2: '2',
        url_3: '3',
    }
    async with session.get(url) as response:
        result = await response.json()
        print(f"{colours[url]}Quote {url_num[url]}: {result}")
        await asyncio.sleep(1)


async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            quote1 = asyncio.create_task(get_quote(url_1, session))
            quote2 = asyncio.create_task(get_quote(url_2, session))
            tasks = [quote1, quote2]
            await asyncio.wait(tasks)
            # print('url1-2')
            await asyncio.create_task(get_quote(url_3, session))
            # print('url3')
            await asyncio.sleep(3)


if __name__ == '__main__':
    asyncio.run(main())
