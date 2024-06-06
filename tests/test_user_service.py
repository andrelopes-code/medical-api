import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from util_functions import get_random_user

from app.models.user import User
from app.schemas.user_schemas import UserCreateRequest, UserUpdateRequest
from app.services.user_service import UserService


async def test_create_user_with_valid_data(async_session: AsyncSession):
    user = UserCreateRequest(**get_random_user().model_dump())
    service = UserService(async_session)
    user = await service.create_user(user)
    assert isinstance(user, User)


async def test_create_user_with_invalid_data(async_session: AsyncSession):
    user = UserCreateRequest(**get_random_user().model_dump())
    user.email = 'invalid@mail'
    service = UserService(async_session)
    with pytest.raises(HTTPException):
        await service.create_user(user)


async def test_update_user_by_email_with_valid_data(async_session: AsyncSession):
    service = UserService(async_session)

    new_user = UserCreateRequest(**get_random_user().model_dump())
    db_new_user = await service.create_user(new_user)

    update_data = UserUpdateRequest(**get_random_user().model_dump())
    updated_user = await service.update_user_by_email(db_new_user.email, update_data)

    assert updated_user.email == update_data.email
    assert updated_user.name == update_data.name
    assert updated_user.phone == update_data.phone


async def test_update_user_by_id_with_valid_data(async_session: AsyncSession):
    service = UserService(async_session)

    new_user = UserCreateRequest(**get_random_user().model_dump())
    db_new_user = await service.create_user(new_user)

    update_data = UserUpdateRequest(**get_random_user().model_dump())
    updated_user = await service.update_user_by_id(db_new_user.id, update_data)

    assert updated_user.email == update_data.email
    assert updated_user.name == update_data.name
    assert updated_user.phone == update_data.phone


async def test_delete_user_by_id(async_session: AsyncSession):
    service = UserService(async_session)

    new_user = UserCreateRequest(**get_random_user().model_dump())
    db_new_user = await service.create_user(new_user)

    await service.delete_user_by_id(db_new_user.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_user_by_id(db_new_user.id)
    assert exc_info.value.status_code == 404


async def test_delete_user_by_email(async_session: AsyncSession):
    service = UserService(async_session)

    new_user = UserCreateRequest(**get_random_user().model_dump())
    db_new_user = await service.create_user(new_user)

    await service.delete_user_by_email(db_new_user.email)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_user_by_email(db_new_user.email)
    assert exc_info.value.status_code == 404
