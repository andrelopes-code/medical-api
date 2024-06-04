from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core import settings

DATABASE_URI = settings.databases.postgres_uri

# Create the async engine for postgres database connection
async_engine = create_async_engine(DATABASE_URI, echo=True, future=True)

# Create a session factory for async sessions
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)


# Generate an AsyncSession instance for interact with database
async def get_db():
    async with async_session() as session:
        yield session


AsyncDBSession = Annotated[AsyncSession, Depends(get_db)]
