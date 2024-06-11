from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import settings

DATABASE_URI = settings.databases.postgres_uri

async_engine = create_async_engine(DATABASE_URI, future=True, pool_size=10, max_overflow=10)
sessionmaker = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    """Creates a new database session and yields it"""
    async with sessionmaker() as session:
        yield session


AsyncSessionDepends = Annotated[AsyncSession, Depends(get_db)]
