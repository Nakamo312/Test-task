from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from config import DB_URL

async_engine = create_async_engine(DB_URL)
async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, class_=AsyncSession, bind=async_engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
