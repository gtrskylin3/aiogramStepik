import asyncio
from random import randint
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType, ChatMemberUpdated
from aiogram.filters import Command, CommandStart, ChatMemberUpdatedFilter, KICKED, and_f
from dotenv import load_dotenv
from admin_filter import IsAdmin, admin_ids

load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

ATTEMPTS = 5

users = {}
user = {
    'in_game': False,
    'secret_number': None,
    'attempts': None,
    'total_games': 0,
    'wins': 0
}




def get_random_num() -> int:
    return randint(1, 100)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        '<b>Привет!</b>\nДавайте сыграем в игру <b>"Угадай число"?</b>\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help', parse_mode='HTML'
    )
    if message.from_user.id not in users:
        users[message.from_user.id] = user
        print(users)

@dp.message(Command(commands=['help']))
async def start(message: Message):
    await message.answer(
        '<b>Правила игры</b>:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть <b>{ATTEMPTS}</b> '
        'попыток\n\nДоступные команды:\n/help - правила '
        'игры и список команд\n/cancel - выйти из игры\n'
        '/stat - посмотреть статистику\n\nДавай сыграем?', parse_mode='HTML'
    )

@dp.message(Command(commands='stat'))
async def stat_cmd(message: Message):
    await message.answer(
        f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
        f'Игр выиграно: {users[message.from_user.id]["wins"]}'
    )

@dp.message(Command(commands='cancel'))
async def cancel_cmd(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы ливнули из игры.\n'
            'захотите сыграть пишите :)'
        )
    else:
        await message.answer('А мы и так не играем.'
                             'GO каточку?')
        
@dp.message(F.text.lower().in_(['да', 'давай',  'сыграем', 'игра',
                                'играть', 'хочу играть']))
async def positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_num()
        users[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer(
            'Я загадал. Ну давай попробуй отгадать\n'
            'жалкий кожанный мешок :)'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )

@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
             'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом q _ q'
        )
    else:
        await message.answer(
            'Мы сейчас в игре. ПИШИ ЧИСЛО ЖАЛКИЙ пользователь :)'
        )

@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def game(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer('на этот раз ты победил (o_0+)'
                                 'сыграем еще :))) или ЗАССАЛ')
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            user['attempts'] -= 1
            await message.answer(f'МОЕ число больше чем {message.text}\nОСТАЛОСЬ ПОПЫТОК {users[message.from_user.id]["attempts"]}')
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            user['attempts'] -= 1
            await message.answer(f'МОЕ число меньше чем {message.text}\nОСТАЛОСЬ ПОПЫТОК {users[message.from_user.id]["attempts"]}')
        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer('GG EZ\nЯ ВЫИГРАЛ ТЕБЯ кожанный мешок :)\nЧисло было: {}\n\nПопробуй еще раз.'.format(user['secret_number']))
    else:
        await message.answer('Ты еще не в игре. Хочешь начать?')

@dp.message(and_f(IsAdmin(admin_ids), Command(commands=['admin'])))
async def answer_if_admins_update(message: Message):
    print(message.from_user.id)
    await message.answer(text='Вы админ')

@dp.message(Command(commands=['admin']))
async def not_admin(message: Message):
    await message.answer('Нету прав для доступа')

@dp.message()
async def other_answer(message:Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )

@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    print(f"Пользователь {event.from_user.full_name, event.from_user.id} Заблокировал бота")
    del users[event.from_user.id]
    print(users)




async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())