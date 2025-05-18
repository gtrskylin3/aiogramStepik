import asyncio
from random import randint
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType, ChatMemberUpdated, PhotoSize
from aiogram.filters import Command, CommandStart, ChatMemberUpdatedFilter, KICKED, and_f
from dotenv import load_dotenv
from filter_n import NumbersInMessage

load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


@dp.message(F.text.lower().startswith('найди числа'), NumbersInMessage())
async def if_numbers(message: Message, numbers: list[int]): # передаем из фильтра
    await message.answer(text=f'Нашел: {", ".join(str(num) for num in numbers)}')

@dp.message(F.text.lower().startswith('найди числа'))
async def if_not_number(message: Message):
    await message.answer(text='НЕ нашел чисел :(')


@dp.message(F.photo[0].as_('ph_min'))
async def photo_send(message: Message, ph_min: PhotoSize):
    await message.answer_photo(photo=ph_min.file_id, caption=str(message.from_user.full_name))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())