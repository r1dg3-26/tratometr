from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import asyncpg
from datetime import timezone, timedelta

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

        try:
            async with pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute("UPDATE users SET balance = balance + $1 WHERE telegram_id = $2", amount, message.from_user.id)
                    await conn.execute("INSERT INTO operations(telegram_id, amount, title) VALUES($1, $2, $3)", 
                                    message.from_user.id, amount, title)
        except Exception as e:
            print(f"DB error: {e}")
            await message.answer("Произошла ошибка, попробуй ещё раз.")
            return

        if amount < 0:
            await message.answer(f"Новая операция: потрачено {abs(amount)} рублей на {title}.")
        else:
            await message.answer(f"Новая операция: получено {amount} рублей из {title}.")
    else: 
        await messages.offerRegister(message)

@router.message(Command("operations"))
async def viewOperations(message: Message, pool: asyncpg.Pool):
    print(f"{message.from_user.id} requested viewing operations.")

    if await sql.isUserExist(pool, message.from_user.id):
        try:
            async with pool.acquire() as conn:
                tz = await conn.fetchval("SELECT timezone FROM users WHERE telegram_id = $1", message.from_user.id)
                operations = await conn.fetch("SELECT * FROM operations WHERE telegram_id = $1 ORDER BY created_at DESC", 
                                            message.from_user.id)
        except Exception as e:
            print(f"DB error: {e}")
            await message.answer("Произошла ошибка, попробуй ещё раз.")
            return
        
        if not operations:
                await message.answer("У тебя пока нет операций.")
                return

        lines = []
        lines.append("Твои операции:")
        for op in operations:
            sign = "📉" if op["amount"] < 0 else "📈"
            dt = op["created_at"].astimezone(timezone(timedelta(hours=int(tz)))).strftime("%d.%m.%Y %H:%M")
            lines.append(f"{sign} #{op['operation_id']} {dt}\n{op['title']}: {op['amount']} руб.")

        await message.answer("\n\n".join(lines))
    else:
        await messages.offerRegister(message)