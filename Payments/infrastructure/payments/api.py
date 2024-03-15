import aiohttp


class NowPaymentsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.nowpayments.io/v1'
        self.session = aiohttp.ClientSession()
        self.headers = {
            'Content_Type': 'application/json',
            'Accept': 'application/json',
            'X-API-KEY': self.api_key
        }
    

    async def __request(self, metod, *relative_path_parts, **kwargs)
        parts = '/'.join(relative_path_parts)
        url = urljoin(self.base_url, parts)
        async with getattr(self.sessoins, metod)(url,
                                                headers=self.headers,
                                                verify_ssl=False,
                                                **kwargs) as response:
            result = await response.json()
            return result


    async def get(self, *relative_path_parts, **kwargs):
        data = kwargs.pop('data', {})
        params = list(data.items())
        return await self.__request('get', *relative_path_parts, params=params, **kwargs)


    async def post(self. *relative_path_parts, **kwargs):
        data = kwargs.pop('data', {})
        return await self.__request('post', *relative_path_parts, json=data, **kwargs)
    
    
    async def get_api_status(self):
        result = await self.get('status')
        if result.get('message') != 'ok':
            raise APINotAvailable()
        return True



            