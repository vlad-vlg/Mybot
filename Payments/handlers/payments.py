from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from handlers.user_handlers import Payments
from infrastructure.payments.api import NowPaymentsAPI
from infrastructure.payments.exception import APINotAvailable
from infrastructure.payments.types import Payment, PaymentStatus


payments_router = Router()


@payments_router.callback_query(Payments.filter())
async def payment(call: CallbackQuery, callback_data: Payments, nowpayments: NowPaymentsAPI):
    try:
        await nowpayments.get_api_status()
    except APINotAvailable as e:
        await call.message.answer(f'API is not available: {e}')
        return

    price = callback_data.my_item_price
    name = callback_data.my_item_name
    my_currency = callback_data.my_currency

    currencies = await nowpayments.get_available_currencies()
    if my_currency not in currencies:
        await call.answer(
            'Данная криптовалюта не поддерживается!\n'
            'Выберите другую валюту платежа.',
            show_alert=True
        )
    payment: Payment = await nowpayments.create_payment(
        price_amount=price,
        price_currency='usd',
        pay_currency=my_currency,
        order_id='123',
        order_description=name
    )
    await call.message.answer(
        f'Пожалуйста, отправьте не менее <b>{payment.pay_amount:.6f} {my_currency.upper()}</b> на адрес ниже.\n'
        f'Ваш ID платежа: <b>{payment.payment_id}</b>.\n'
        f'Нажмите на команду /check_payment_{payment.payment_id}, '
        f'чтобы проверить статус транзакции.\n\n'
        f'Адрес: <code>{payment.pay_address}</code>\n'
        f'Сумма: <code>{payment.pay_amount:.6f}</code>'
    )
    await call.answer()


@payments_router.message(F.text.regexp(r'^/check_payment_(\d+)$').as_('payment_id_match'))
async def check_payment(message: Message, nowpayments: NowPaymentsAPI, payment_id_match):
    payment_id = payment_id_match.group(1)
    payment_status = await nowpayments.get_payment_status(payment_id)

    if payment_status.payment_status in (PaymentStatus.CONFIRMED, PaymentStatus.FINISHED):
        await message.answer(f'Платеж {payment_id} подтвержден.')
    else:
        await message.answer(f'Платеж {payment_id} еще не подтвержден!')
