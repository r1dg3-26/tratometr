import asyncpg

async def isUserExist(pool: asyncpg.Pool, telegram_id: int):
    async with pool.acquire() as conn:
        return await conn.fetchval("SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id = $1)", telegram_id)