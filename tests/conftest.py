import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

from app.core import settings
from app.core.databases.postgres import async_engine, sessionmaker
from app.core.main import app
from app.core.security.security import SecurityService


async def clear_all_tables(conn):
    """This function clears all tables in the database"""
    from app.models import Address, Appointment, Doctor, Patient, User

    models = [
        Appointment,
        Doctor,
        Patient,
        Address,
        User,
    ]
    for model in models:
        await conn.execute(delete(model))


@pytest_asyncio.fixture(scope='function')
def json_headers():
    token = SecurityService.create_access_token(data_to_encode=dict(username='test', password='test'))
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}


@pytest_asyncio.fixture(scope='function')
def authorization():
    token = SecurityService.create_access_token(data_to_encode=dict(username='test', password='test'))
    return {'Authorization': f'Bearer {token}', 'accept': 'application/json'}


@pytest_asyncio.fixture(scope='function')
async def async_client():
    """Creates an async client to interact with the API"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url=f'http://{settings.api_v1_prefix}') as client:
        yield client


@pytest_asyncio.fixture(scope='function')
async def async_session():
    """Creates an async session for testing purposes and clears all tables after each test"""
    try:
        async with sessionmaker() as sess:
            yield sess
            await sess.rollback()

        async with async_engine.begin() as conn:
            await clear_all_tables(conn)

    finally:
        await async_engine.dispose()
