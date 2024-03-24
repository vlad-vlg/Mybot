from aiogram import BaseMiddleware

from Database.infrastructure.database.requests import get_user, create_and_get_user


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, aiomysql_pool):
        super().__init__()
        self.aiomysql_pool = aiomysql_pool

    async def __call__(self, handler, event, data):
        async with self.aiomysql_pool.acquire() as db_connection:
            user = await get_user(db_connection, event.from_user.id)
            if not user:
                user = await create_and_get_user(db_connection,
                                                 telegram_id=event.from_user.id,
                                                 username=event.from_user.username,
                                                 full_name=event.from_user.full_name)
            data.update({'db_connection': db_connection, 'user': user})
            await handler(event, data)
