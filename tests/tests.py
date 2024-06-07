import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.databases.postgres import get_db


@pytest.mark.asyncio
async def test_get_db_function_is_working_correctly():
    async for session in get_db():
        assert session is not None
        assert session.is_active
        assert isinstance(session, AsyncSession)
