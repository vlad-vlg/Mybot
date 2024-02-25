import aiohttp
import asyncio


url_1 = 'https://api.gameofthronesquotes.xyz/v1/random'
url_2 = 'https://lucifer-quotes.vercel.app/api/quotes'
url_3 = 'https://strangerthings-quotes.vercel.app/api/quotes'


async def quote_1():
    url = 'https://api.gameofthronesquotes.xyz/v1/random'
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url) as response:
                result = await response.json()
                print(f"\33[31m Quote1: {result}")
            await asyncio.sleep(5)


async def quote_2():
    url = 'https://lucifer-quotes.vercel.app/api/quotes'
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url) as response:
                result = await response.json()
                print(f"\33[34m Quote2: {result}")
            await asyncio.sleep(5)


async def quotes(url):
    colours = {
        url_1: '\33[32m',
        url_2: '\33[34m',
        url_3: '\33[33m',
    }
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url) as response:
                result = await response.json()
                print(f"{colours[url]} Quote: {result}")
            await asyncio.sleep(5)


async def main():
    tasks = [quotes(url_1), quotes(url_2), quotes(url_3)]
    await asyncio.gather(*tasks)


asyncio.run(main())
