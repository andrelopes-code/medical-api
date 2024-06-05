import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core import settings
from app.core.databases.postgres import async_engine
from app.core.main import app
from app.models import SQLModel

MODELS = SQLModel.__subclasses__()


async def clear_all_tables(conn):
    """This function clears all tables in the database"""
    for model in MODELS:
        await conn.execute(delete(model))


@pytest_asyncio.fixture(scope='function')
async def async_client():
    """Creates an async client to interact with the API"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url=f'http://{settings.api_v1_prefix}') as client:
        yield client


@pytest_asyncio.fixture(scope='function')
async def async_session():
    """Creates an async session for testing purposes and clears all tables after each test"""
    session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

    async with session() as sess:
        yield sess

    async with async_engine.begin() as conn:
        await clear_all_tables(conn)

    await async_engine.dispose()
