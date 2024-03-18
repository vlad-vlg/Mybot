from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, Document
from aiogram.utils.media_group import MediaGroupBuilder


payments_router = Router()


@payments_router.message(Command('payment')
async def payment(message: Message, nowpayments: NowPaymentsAPI):
    try:
        await nowpayments.get_api_status()
    except APINotAvailable as e:
        await message.answer(f'API is not available: {e}')
        return


    price = 10
    currency = 'btc'
    payment: Payment = await nowpayments.create_payment(
        price_amount=price,
        price_currency='usd',
        pay_currency=currency,
        order_id='123',
        order_description=f'{message.from_user.id}'
    )
    await message.answer(
        f''
        f''
        f''
        f''
    )
