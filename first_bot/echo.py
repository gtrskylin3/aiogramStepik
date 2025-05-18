import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def start(message: Message):
    await message.answer('Я все повторяю за тобой хихихихи')

@dp.message(Command(commands=['help']))
async def help(message: Message):
    await message.answer('Введи чето лол')

# @dp.message(F.content_type == ContentType.TEXT)
# async def text_echo(message: Message):
#     try:
#         await message.reply(text=message.text)
#     except:
#         await message.reply(text='Я НИЧЕГО НЕ ПОНЯЛ')

# @dp.message(F.content_type == ContentType.PHOTO)
# async def photo_echo(message: Message):
#     await message.answer_photo(photo=message.photo[0].file_id)
    

# @dp.message(F.sticker)
# async def sticker_echo(message: Message):
#     await message.answer_sticker(sticker=message.sticker.file_id)

@dp.message()
async def echo_bot(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer('Упс...')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())