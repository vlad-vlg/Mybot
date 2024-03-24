from aiogram import BaseMiddleware


class PaymentsMiddleware(BaseMiddleware):
    def __init__(self, nowpayments):
        super().__init__()
        self.nowpayments = nowpayments

    async def __call__(self, handler, event, data):
        data.update({'nowpayments': self.nowpayments})
        await handler(event, data)
