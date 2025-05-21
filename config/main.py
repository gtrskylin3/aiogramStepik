import config.config as cfg
from aiogram import Bot, Dispatcher


config = cfg.load_config('C:/Users/daniil/PycharmProjects/stepikAiogram/aiogramStepik/config/.env')

bot = Bot(token=config.tg_bot.token)
dp = Dispatcher()

some_var = 1
some_text = 'asdasd'
# dp['my_int_var'] = some_var
# dp['my_text_var'] = some_text

dp.workflow_data({'my_int': some_var,
                  'my_str': some_text})

# @dp.message()
# async def process_start_cmd(my_int, my_str):
#     await message.answer(text=str(my_int))