from aiogram.filters import Filter
from aiogram.types import Message
class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types
    
    async def __call__(self, message: Message) -> bool:
        return message.chat.type in self.chat_types
