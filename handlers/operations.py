from aiogram import Router, F
from aiogram.types import Message
import asyncpg

from helpers import sql, messages

router = Router()

@router.message(F.text.startswith("-") | F.text.startswith("+"))
async def createOperation(message: Message, pool: asyncpg.Pool):
    print(f"{message.from_user.id} requested creating operation.")

    if await sql.isUserExist(pool, message.from_user.id):
        hint = "правильно \"+сумма товар\\услуга\" или \"-сумма товар\\услуга\", например -30 доширак"

        parts = message.text.split(maxsplit=1)

        if len(parts) != 2:
            await message.answer(f"Неверный формат операции, {hint}")
            return

        try:
            amount = float(parts[0])
        except ValueError:
            await message.answer(f"Неверный формат суммы, {hint}")
            return
        
        title = parts[1]

        async with pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("UPDATE users SET balance = balance + $1 WHERE telegram_id = $2", amount, message.from_user.id)
                await conn.execute("INSERT INTO operations(telegram_id, amount, title) VALUES($1, $2, $3)", message.from_user.id, amount, title)

        if amount < 0:
            await message.answer(f"Новая операция: потрачено {abs(amount)} рублей на {title}.")
        else:
            await message.answer(f"Новая операция: получено {amount} рублей из {title}.")
    else: 
        await messages.offerRegister(message)