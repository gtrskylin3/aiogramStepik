import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from database.models import Base

# engine = create_async_engine(os.getenv('DB_LITE'), echo=True)
engine = create_async_engine(os.getenv('DB_URL'), echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# async def m():
#     async with session_maker() as session:
#         session.execute

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Что происходит:
# Создается движок (engine) для подключения к БД
# Создается фабрика сессий (session_maker)
# create_db создает все таблицы в БД через миграции
# Аналогия:
# session_maker - как конвейер, производящий новые сессии (рабочие сессии для БД)