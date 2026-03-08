import os
import asyncio
from aiogram import Bot, Dispatcher
import asyncpg

from handlers import router

async def main():
    print("Warming up...")

    pool = None
    try:
        token = os.environ["TG_TOKEN"]
        bot = Bot(token=token)
        dp = Dispatcher()

        pool = await asyncpg.create_pool(
            host=os.environ["PSQL_IP"],
            port=int(os.environ["PSQL_PORT"]),
            user=os.environ["PSQL_USER"],
            password=os.environ["PSQL_PASS"],
            database=os.environ["PSQL_DB"],
            min_size=2,
            max_size=10
        )

        dp["pool"] = pool
        dp.include_router(router)

        print("Ready!")
        await dp.start_polling(bot)
    finally:
        if pool:
            print("Bye!")
            await pool.close()

if __name__ == "__main__":
    asyncio.run(main())