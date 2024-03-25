async def create_and_get_user(
        db_connection,
        telegram_id: int,
        full_name: str,
        username: str = None
):
    cursor = await db_connection.cursor()
    await cursor.execute(
        'INSERT INTO users (telegram_id, full_name, username) '
        'VALUES (%s, %s, %s) ',
        (telegram_id, full_name, username)
    )
    await db_connection.commit()

    await cursor.execute(
        'SELECT telegram_id, full_name, username FROM users WHERE telegram_id = %s',
        (telegram_id,)
    )
    user = await cursor.fetchone()
    await cursor.close()
    return user


async def get_user(db_connection, telegram_id: int):
    cursor = await db_connection.cursor()
    await cursor.execute(
        'SELECT telegram_id, full_name, username FROM users WHERE telegram_id = %s',
        (telegram_id,)
    )
    user = await cursor.fetchone()
    await cursor.close()
    return user


async def create_transaction(
        db_connection,
        user_id,
        usd_amount,
        pay_amount,
        currency,
        pay_address,
        payment_id,
        order_id: int = None,
        comment: str = None
):
    cursor = await db_connection.cursor()
    await cursor.execute(
        'INSERT INTO transactions (user_id, usd_amount, pay_amount, currency, pay_address, payment_id, order_id, comment) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ',
        (user_id, usd_amount, pay_amount, currency, pay_address, payment_id, order_id, comment)
    )
    await db_connection.commit()
    await cursor.close()


async def get_balance(db_connection, user_id):
    cursor = await db_connection.cursor()
    await cursor.execute(
        'SELECT SUM(usd_amount) FROM transactions WHERE user_id = %s',
        (user_id,)
    )
    (balance, ) = await cursor.fetchone()
    await cursor.close()
    return balance


async def create_new_order(db_connection, user_id, amount: int, order_info: str):
    cursor = await db_connection.cursor()
    await cursor.execute(
        'INSERT INTO orders (user_id, amount, order_info) '
        'VALUES (%s, %s, %s) ',
        (user_id, amount, order_info)
    )
    order_id = cursor.lastrowid
    await db_connection.commit()
    await cursor.close()
    return order_id


async def get_order(db_connection, order_id: int):
    cursor = await db_connection.cursor()
    await cursor.execute(
        'SELECT amount, paid FROM orders WHERE id = %s',
        (order_id,)
    )
    order = await cursor.fetchone()
    await cursor.close()
    return order


async def update_transaction(db_connection, payment_id: int, status: bool = True):
    cursor = await db_connection.cursor()
    await cursor.execute(
        'UPDATE transactions SET paid = %s WHERE payment_id = %s',
        (status, payment_id)
    )
    await db_connection.commit()
    await cursor.close()


async def get_order_id_from_tx(db_connection, payment_id: int):
    cursor = await db_connection.cursor()
    await cursor.execute(
        'SELECT order_id FROM transactions WHERE payment_id = %s',
        (payment_id,)
    )
    order_id = await cursor.fetchone()
    await cursor.close()
    return order_id


async def confirm_order(db_connection, order_id: int):
    cursor = await db_connection.cursor()
    await cursor.execute(
        'UPDATE orders SET paid = True WHERE id = %s',
        (order_id,)
    )
    await db_connection.commit()
    await cursor.close()


async def get_user_id_from_tx(db_connection, payment_id: int):
    cursor = await db_connection.cursor()
    await cursor.execute(
        'SELECT user_id FROM transactions WHERE payment_id = %s',
        (payment_id,)
    )
    user_id = await cursor.fetchone()
    await cursor.close()
    return user_id


