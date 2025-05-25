from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Dict, Awaitable, Any
from sqlalchemy.ext.asyncio.session import async_sessionmaker


class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool # сессия будет в каждом хэндлере
    
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with self.session_pool() as session:
            data['session'] = session
            return await handler(event, data)

# класс который при иницализации создает новую асинхроную сессию БД для каждого 
# входящего запроса  
# а при вызове получает хендлер ивент и дату(наш фсм) и 
# Сессия добавляется в контекст (data['session']) и становится доступна во всех обработчиках
# Как работает:
# При каждом сообщении/действии пользователя создается новая сессия
# Сессия передается в обработчик через параметр data
# После завершения обработки сессия автоматически закрывается
# Аналогия: Представь, что это как раздача инструментов (сессий БД)
# рабочим (хэндлерам) перед началом работы. 
# Каждый рабочий получает свой набор инструментов.



























# class CounterMiddleware(BaseMiddleware):
#     def __init__(self) -> None: # при старте бота
#         self.counter = 0 

#     async def __call__(
#         self,
#         handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
#         event: Message,
#         data: Dict[str, Any]
#     ) -> Any:
#         self.counter += 1
#         data['counter'] = self.counter
#         return await handler(event, data)

