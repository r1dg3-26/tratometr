from aiogram import Router, F
from aiogram.filters import CommandStart, Command
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
        try:
            async with pool.acquire() as conn:
                await conn.execute("INSERT INTO users(telegram_id) VALUES($1) ON CONFLICT DO NOTHING", message.from_user.id)
        except Exception as e:
            print(f"DB error: {e}")
            await message.answer("Произошла ошибка, попробуй ещё раз.")
            return
        
        await message.answer(f"Привет, {message.from_user.full_name}!\n\n"
                                "По умолчанию используется МСК (UTC+3).\n\n"
                                "Чтобы задать часовой пояс, отличный от МСК, напиши \"/timezone число\", например /timezone 5" 
                                " - это ЕКБ\n\n"
                                "Чтобы задать начальный баланс, напиши \"/balance сумма\", например /balance 100000")

@router.message(Command("timezone"))
async def setTimezone(message: Message, pool: asyncpg.Pool):
    print(f"{message.from_user.id} requested setting timezone.")

    if await sql.isUserExist(pool, message.from_user.id):
        parts = message.text.split()

        if len(parts) != 2:
            await message.answer("Укажи часовой пояс, например: /timezone 5")
            return

        try:
            timezone = int(parts[1])
        except ValueError:
            await message.answer("Неверный формат часового пояса, правильно \"/timezone число\", например /timezone 5")
            return
        
        if not -12 <= timezone <= 14:
            await message.answer("Такого часового пояса не существует!")
            return

        try:
            async with pool.acquire() as conn:
                await conn.execute("UPDATE users SET timezone = $1 WHERE telegram_id = $2", timezone, message.from_user.id)
        except Exception as e:
            print(f"DB error: {e}")
            await message.answer("Произошла ошибка, попробуй ещё раз.")
            return

        await message.answer(f"Задан часовой пояс: {timezone}.")
    else: 
        await messages.offerRegister(message)

@router.message(Command("balance"))
async def setBalance(message: Message, pool: asyncpg.Pool):
    print(f"{message.from_user.id} requested setting balance.")

    if await sql.isUserExist(pool, message.from_user.id):
        parts = message.text.split()

        if len(parts) != 2:
            await message.answer("Укажи сумму, например: /balance 100000")
            return

        try:
            balance = float(parts[1])
        except ValueError:
            await message.answer("Неверный формат суммы, правильно \"/balance сумма\", например /balance 100000")
            return
        
        try:
            async with pool.acquire() as conn:
                await conn.execute("UPDATE users SET balance = $1 WHERE telegram_id = $2", balance, message.from_user.id)
        except Exception as e:
            print(f"DB error: {e}")
            await message.answer("Произошла ошибка, попробуй ещё раз.")
            return

        await message.answer(f"Задан баланс: {balance} рублей.")
    else: 
        await messages.offerRegister(message)