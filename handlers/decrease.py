from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.startswith("-"))
async def start(message: Message):
    print(str(message.from_user.id) + " requested decreasing balance")
    await message.answer("Decreased!")