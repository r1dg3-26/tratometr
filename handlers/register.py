from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import asyncpg

from helpers import sql, messages

router = Router()

@router.message(CommandStart())
async def start(message: Message, pool: asyncpg.Pool):
    print(f"{message.from_user.id} requested /start.")

    if await sql.isUserExist(pool, message.from_user.id):
        await message.answer(f"Привет, {message.from_user.full_name}!")
    else:
        async with pool.acquire() as conn:
            await conn.execute("INSERT INTO users(telegram_id) VALUES($1) ON CONFLICT DO NOTHING", message.from_user.id)
        await message.answer(f"Привет, {message.from_user.full_name}!\nЧтобы задать начальный баланс, напиши \"баланс сумма\", например баланс 100000")

@router.message(F.text.lower().startswith("баланс"))
async def setBalance(message: Message, pool: asyncpg.Pool):
    print(f"{message.from_user.id} requested setting balance.")

    if await sql.isUserExist(pool, message.from_user.id):
        parts = message.text.split()

        if len(parts) != 2:
            await message.answer("Укажи сумму, например: баланс 100000")
            return

        try:
            balance = float(parts[1])
        except ValueError:
            await message.answer("Неверный формат суммы, правильно \"баланс сумма\", например баланс 100000")
            return

        async with pool.acquire() as conn:
            await conn.execute("UPDATE users SET balance = $1 WHERE telegram_id = $2", balance, message.from_user.id)

        await message.answer(f"Задан баланс: {balance} рублей.")
    else: 
        await messages.offerRegister(message)