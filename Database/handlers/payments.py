import json
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from Database.handlers.user_handlers import Payments
from Database.infrastructure.database.requests import create_new_order, get_order, create_transaction, \
    update_transaction, get_order_id_from_tx, confirm_order, get_balance, get_user_id_from_tx
from infrastructure.payments.api import NowPaymentsAPI
from infrastructure.payments.exception import APINotAvailable
from infrastructure.payments.types import Payment, PaymentStatus

payments_router = Router()
admins_router = Router()


# @payments_router.message(Command('create_order'))
# async def cmd_create_order(message: Message, db_connection):
#     order_info = {
#         'items': [
#             {
#                 'name': 'Test_item',
#                 'price': 15.99,
#                 'quantity': 1,
#             }
#         ],
#         'some_other_info': 'some_other_info'
#     }
#     amount = 25
#     order_id = await create_new_order(db_connection, message.from_user.id, amount, json.dumps(order_info))
#     await message.answer(
#         f'Создан заказ с ID {order_id}. Для оплаты нажмите /pay_order_{order_id}'
#     )
#
#
# @payments_router.message(F.text.regexp(r'^/pay_order_(\d+)$').as_('order_id_match'))
# async def cmd_pay_order(message: Message, nowpayments: NowPaymentsAPI, order_id_match, db_connection):
#     order_id = int(order_id_match.group(1))
#     amount, paid_status = await get_order(db_connection, order_id)
#     if paid_status:
#         await message.answer(f'Заказ № {order_id} уже оплачен')
#         return
#
#     try:
#         await nowpayments.get_api_status()
#     except APINotAvailable as e:
#         await message.answer(f'API is not available: {e}')
#         return
#
#     my_currency = 'btc'
#     payment: Payment = await nowpayments.create_payment(
#         price_amount=float(amount),
#         price_currency='usd',
#         pay_currency=my_currency,
#         order_id='123',
#         order_description='test'
#     )
#     await create_transaction(db_connection,
#                              message.from_user.id,
#                              amount,
#                              payment.pay_amount,
#                              my_currency,
#                              payment.pay_address,
#                              payment.payment_id,
#                              order_id,
#                              'Пополнение баланса'
#                              )
#     await create_transaction(db_connection,
#                              message.from_user.id,
#                              -amount,
#                              payment.pay_amount,
#                              my_currency,
#                              payment.pay_address,
#                              payment.payment_id,
#                              order_id,
#                              'Снятие средств за заказ'
#                              )
#     await message.answer(
#         f'Пожалуйста, отправьте не менее <b>{payment.pay_amount:.6f} {my_currency.upper()}</b> на адрес ниже.\n'
#         f'Ваш ID платежа: <b>{payment.payment_id}</b>.\n'
#         f'Нажмите на команду /check_payment_{payment.payment_id}, '
#         f'чтобы проверить статус транзакции.\n\n'
#         f'Адрес: <code>{payment.pay_address}</code>\n'
#         f'Сумма: <code>{payment.pay_amount:.6f}</code>'
#     )
@payments_router.callback_query(Payments.filter())
async def payment(call: CallbackQuery, callback_data: Payments, nowpayments: NowPaymentsAPI, db_connection):
    order_id = callback_data.order_id
    name = callback_data.my_item_name
    my_currency = callback_data.my_currency
    amount, paid_status = await get_order(db_connection, order_id)

    if paid_status:
        await call.message.answer(f'Заказ № {order_id} уже оплачен')
        return

    try:
        await nowpayments.get_api_status()
    except APINotAvailable as e:
        await call.message.answer(f'API is not available: {e}')
        return

    currencies = await nowpayments.get_available_currencies()
    if my_currency not in currencies:
        await call.answer(
            'Данная криптовалюта не поддерживается!\n'
            'Выберите другую валюту платежа.',
            show_alert=True
        )
    payment: Payment = await nowpayments.create_payment(
        price_amount=float(amount),
        price_currency='usd',
        pay_currency=my_currency,
        order_id=str(order_id),
        order_description=name
    )
    await create_transaction(
        db_connection,
        call.from_user.id,
        amount,
        payment.pay_amount,
        my_currency,
        payment.pay_address,
        payment.payment_id,
        order_id,
        'Пополнение баланса'
    )
    await create_transaction(
        db_connection,
        call.from_user.id,
        -amount,
        payment.pay_amount,
        my_currency,
        payment.pay_address,
        payment.payment_id,
        order_id,
        'Снятие средств за заказ'
    )
    await call.message.answer(
        f'Пожалуйста, отправьте не менее <b>{payment.pay_amount:.6f} {my_currency.upper()}</b> на адрес ниже.\n'
        f'Ваш ID платежа: <code><b>{payment.payment_id}</b></code>.\n'
        f'Нажмите на команду /check_payment_{payment.payment_id}, '
        f'чтобы проверить статус транзакции.\n\n'
        f'Адрес: <code>{payment.pay_address}</code>\n'
        f'Сумма: <code>{payment.pay_amount:.6f}</code>'
    )
    await call.answer()


@payments_router.message(F.text.regexp(r'^/check_payment_(\d+)$').as_('payment_id_match'))
async def check_payment(message: Message, nowpayments: NowPaymentsAPI, payment_id_match, db_connection):
    payment_id = payment_id_match.group(1)
    payment_status = await nowpayments.get_payment_status(payment_id)

    if payment_status.payment_status in (PaymentStatus.CONFIRMED, PaymentStatus.FINISHED):
        await update_transaction(db_connection, payment_id)
        order_id = await get_order_id_from_tx(db_connection, payment_id)
        await confirm_order(db_connection, order_id)
        await message.answer(
            f'Платеж <code>{payment_id}</code> подтвержден.\n'
            f'Оплата заказа № <code>{order_id}</code> прошла успешно.'
        )
    else:
        await message.answer(
            f'Платеж <code>{payment_id}</code> еще не подтвержден!\n'
            f'Статус: <code>{payment_status.payment_status}</code>.'
        )


@payments_router.message(Command('get_balance'))
async def cmd_get_balance(message: Message, db_connection):
    balance = await get_balance(db_connection, message.from_user.id)
    await message.answer(f'Ваш баланс: {balance:.2f}')


@admins_router.message(F.text.regexp(r'^/approve_payment_(\d+)_(\d+)$').as_('order_match'))
async def cmd_approve_payment(message: Message, bot: Bot, nowpayments: NowPaymentsAPI,
                              order_match, db_connection):
    order_id = order_match.group(1)
    payment_id = order_match.group(2)

    amount, paid_status = await get_order(db_connection, order_id)

    if paid_status:
        await message.answer(f'Заказ № {order_id} уже оплачен')
        return

    await update_transaction(db_connection, payment_id)
    await confirm_order(db_connection, order_id)
    await message.answer(
        f'Платеж <code>{payment_id}</code> подтвержден.\n'
        f'Оплата заказа № <code>{order_id}</code> прошла успешно.'
    )
    (user_id, ) = await get_user_id_from_tx(db_connection, payment_id)
    print(user_id)
    await bot.send_message(user_id,
                           text=f'Ваш Платеж <code>{payment_id}</code> подтвержден.\n'
                                f'Оплата Вашего заказа № <code>{order_id}</code> прошла успешно.'
                           )


# @payments_router.message(Command('add_payment'))
# async def cmd_approve_payment(message: Message, bot: Bot, db_connection, user_id, usd_amount, pay_amount, currency,
#                               pay_address, payment_id):
#     await create_transaction(
#         db_connection,
#         user_id,
#         usd_amount,
#         pay_amount,
#         currency,
#         pay_address,
#         payment_id
#     )
#     await create_transaction(
#         db_connection,
#         user_id,
#         usd_amount,
#         pay_amount,
#         currency,
#         pay_address,
#         payment_id
#     )
#
#     await update_transaction(db_connection, payment_id)
#     # order_id = await get_order_id_from_tx(db_connection, payment_id)
#     # user_id = await get_user_id_from_tx(db_connection, payment_id)
#     # await confirm_order(db_connection, order_id)
#     await message.answer(
#         f'Платеж <code>{payment_id}</code> подтвержден.\n'
# #        f'Оплата заказа № <code>{order_id}</code> прошла успешно.'
#     )
#     await bot.send_message(user_id,
#                            text=f'Ваш Платеж <code>{payment_id}</code> подтвержден.\n'
#                                 f'Оплата Вашего заказа № <code>{order_id}</code> прошла успешно.'
#                            )
