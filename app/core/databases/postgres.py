from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core import settings

DATABASE_URI = settings.databases.postgres_uri

async_engine = create_async_engine(DATABASE_URI, future=True)

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():  # pragma: no cover | function is used in tests
    async with async_session() as session:
        yield session


AsyncDBSession = Annotated[AsyncSession, Depends(get_db)]
