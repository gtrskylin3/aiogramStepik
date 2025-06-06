import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.strategy import FSMStrategy
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from database.engine import create_db, drop_db, session_maker
from middlewares.dp import DataBaseSession


from handlers.admin_private import admin_router
from handlers.user_private import user_private_router
from handlers.user_group import user_group_router

from common.bot_cmds_list import private

# ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(fsm_strategy = FSMStrategy.USER_IN_CHAT)

bot.my_admins_id = []

dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_router)

async def on_startup(bot):

    run_param = False
    if run_param:
        await drop_db()

    await create_db()

async def on_shutdown(bot):
    print('бот лег')



async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
# Middleware регистрируется в диспетчере
# При каждом сообщении создается новая сессия
# Сессия автоматически передается в хэндлеры как параметр session
# Важно: Обрати внимание, что параметр session в хэндлере автоматически заполняется благодаря middleware.
    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())