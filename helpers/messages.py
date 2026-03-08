from aiogram.types import Message

async def offerRegister(message: Message):
    await message.answer("Я не нашел тебя в своих списках. Пожалуйста, пройди регистрацию командой /start")