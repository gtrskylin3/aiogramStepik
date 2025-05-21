from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from lexicon.lexicon import LEXICON_RU
from .admin_filter import IsAdmin, admin_ids


router = Router()
router.message.filter(IsAdmin(admin_ids=
                              admin_ids))

@router.message(Command(commands='admin'))
async def isadmin(message: Message):
    await message.answer('админ')
