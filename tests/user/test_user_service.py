import pytest
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from util_functions import get_random_user

from app.models.user import User
from app.schemas.user_schemas import UserUpdateRequest
from app.services.user_service import UserService


async def test_create_user_with_valid_data(async_session: AsyncSession):
    create_data = get_random_user()
    service = UserService(async_session)
    create_data = await service.create_user(create_data)
    assert isinstance(create_data, User)


async def test_create_user_with_invalid_data(async_session: AsyncSession):
    create_data = get_random_user()
    create_data.user.email = 'invalid@mail'
    service = UserService(async_session)
    with pytest.raises(HTTPException):
        await service.create_user(create_data)


async def test_update_user_by_email_with_valid_data(async_session: AsyncSession):
    service = UserService(async_session)

    new_user = get_random_user()
    db_new_user = await service.create_user(new_user)

    update_user = get_random_user().user

    update_data = UserUpdateRequest(name=update_user.name, email=update_user.email, phone=update_user.phone)
    updated_user = await service.update_user_by_email(db_new_user.email, update_data)

    assert updated_user.email == update_data.email
    assert updated_user.name == update_data.name
    assert updated_user.phone == update_data.phone


async def test_update_user_by_id_with_valid_data(async_session: AsyncSession):
    service = UserService(async_session)

    new_user = get_random_user()
    db_new_user = await service.create_user(new_user)
    update_user = get_random_user().user

    update_data = UserUpdateRequest(name=update_user.name, email=update_user.email, phone=update_user.phone)
    updated_user = await service.update_user_by_id(db_new_user.id, update_data)

    assert updated_user.email == update_data.email
    assert updated_user.name == update_data.name
    assert updated_user.phone == update_data.phone


@pytest.mark.skip(reason='Needs cascade delete in database')
async def test_delete_user_by_id(async_session: AsyncSession):
    service = UserService(async_session)

    new_user = get_random_user()
    db_new_user = await service.create_user(new_user)

    await service.delete_user_by_id(db_new_user.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_user_by_id(db_new_user.id)
    assert exc_info.value.status_code == 404


@pytest.mark.skip(reason='Needs cascade delete in database')
async def test_delete_user_by_email(async_session: AsyncSession):
    service = UserService(async_session)

    new_user = get_random_user()
    db_new_user = await service.create_user(new_user)

    await service.delete_user_by_email(db_new_user.email)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_user_by_email(db_new_user.email)
    assert exc_info.value.status_code == 404
