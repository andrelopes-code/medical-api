import asyncio

import pytest
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from util_functions import get_random_user

from app.core.databases.postgres import sessionmaker
from app.core.security.auth import AuthService
from app.services.user_service import UserService

auth_service = AuthService()


async def test_auth_service_with_valid_data(async_session: AsyncSession):
    create_data = get_random_user()
    user_service = UserService(async_session)
    created_user = await user_service.create_user(create_data)
    create_data = await auth_service.login_user(email=created_user.email, password=create_data.user.password)
    assert create_data


async def test_auth_service_with_wrong_password(async_session: AsyncSession):
    create_data = get_random_user()
    user_service = UserService(async_session)
    created_user = await user_service.create_user(create_data)
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.login_user(email=created_user.email, password='wrong')

    assert exc_info.value.status_code == 401


async def test_auth_service_with_wrong_email(async_session: AsyncSession):
    create_data = get_random_user()
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.login_user(email=create_data.user.email, password='inexistentuser')

    assert exc_info.value.status_code == 401


async def test_auth_service_with_no_data(async_session: AsyncSession):
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.login_user(email='', password='')

    assert exc_info.value.status_code == 401


async def test_auth_service_with_no_password(async_session: AsyncSession):
    user = get_random_user()
    user_service = UserService(async_session)
    created_user = await user_service.create_user(user)
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.login_user(email=created_user.email, password='')

    assert exc_info.value.status_code == 401


async def test_auth_service_with_no_email(async_session: AsyncSession):
    user = get_random_user()
    user_service = UserService(async_session)
    created_user = await user_service.create_user(user)
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.login_user(email='', password=created_user.password)

    assert exc_info.value.status_code == 401


async def test_auth_service_with_uppercase_email(async_session: AsyncSession):
    create_data = get_random_user()
    user_service = UserService(async_session)
    created_user = await user_service.create_user(create_data)
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.login_user(email=created_user.email.upper(), password=create_data.user.password)

    assert exc_info.value.status_code == 401


async def test_auth_service_multiple_users(async_session: AsyncSession):

    async def create_and_login_user(create_data):
        async with sessionmaker() as session:
            auth_service = AuthService()
            user_service = UserService(session)
            created_user = await user_service.create_user(create_data)
            return await auth_service.login_user(email=created_user.email, password=create_data.user.password)

    tasks = [create_and_login_user(get_random_user()) for _ in range(5)]

    result = await asyncio.gather(*tasks, return_exceptions=True)

    for r in result:
        assert r
