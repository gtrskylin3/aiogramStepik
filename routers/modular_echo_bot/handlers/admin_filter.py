from environs import Env
from dotenv import load_dotenv
from aiogram.filters import BaseFilter
from aiogram.types import Message

load_dotenv()

env = Env()
env.read_env(path='C:/Users/daniil/PycharmProjects/stepikAiogram/aiogramStepik/.env',
             override=True)

admin_ids: list[int] = [int(env('ADMIN'))]
print(admin_ids)

class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids
    
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids