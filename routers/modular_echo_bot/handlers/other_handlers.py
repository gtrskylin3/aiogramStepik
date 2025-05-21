from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import Command, CommandStart

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=LEXICON_RU['/start'])

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message()
async def echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except  TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])

