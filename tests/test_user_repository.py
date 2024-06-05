from datetime import datetime

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from util_functions import get_random_user

from app.core.security import SecurityManager
from app.models.user import User
from app.repository.user_repository import UserRepository


@pytest.mark.asyncio
async def test_user_updated_at_field_is_updating_correctly(async_session: AsyncSession):

    user = get_random_user()

    user = User.model_validate(user)

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    old_updated_at = user.updated_at

    user.name = 'John Smith'

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    assert user.updated_at > old_updated_at


@pytest.mark.asyncio
async def test_user_repository_create_user_and_get_user(async_session: AsyncSession):
    repository = UserRepository(async_session)

    user = get_random_user()

    created_user = await repository.create_user(user)
    assert isinstance(created_user, User)

    db_user = await repository.get_user_by_id(created_user.id)
    assert db_user == created_user

    assert created_user.password != user.password


@pytest.mark.asyncio
async def test_get_user_with_invalid_user_id(async_session: AsyncSession):
    repository = UserRepository(async_session)

    db_user = await repository.get_user_by_id(999)
    assert db_user is None


@pytest.mark.asyncio
async def test_update_user_with_valid_data(async_session: AsyncSession):
    repository = UserRepository(async_session)

    user = get_random_user()

    created_user = await repository.create_user(user)
    assert isinstance(created_user, User)

    updates = [
        dict(name='Fazz Name', email='fazzuser@email.com'),
        dict(gender='other', phone='+5521977776666'),
        dict(
            name='Bar Name Name',
            email='barbar@outlook.com',
            gender='female',
            user_type='doctor',
            birthdate=datetime.now(),
        ),
    ]

    for update_data in updates:
        updated_user = await repository.update_user_by_id(created_user.id, update_data)

        for field, value in update_data.items():
            if value is not None:
                assert getattr(updated_user, field) == value


@pytest.mark.asyncio
async def test_delete_user_by_id(async_session: AsyncSession):
    repository = UserRepository(async_session)

    user = get_random_user()

    fake_user = await repository.delete_user_by_id(999)
    assert fake_user is None

    created_user = await repository.create_user(user)
    assert isinstance(created_user, User)

    deleted_user = await repository.delete_user_by_id(created_user.id)
    assert deleted_user == created_user

    db_user = await repository.get_user_by_id(created_user.id)
    assert db_user is None


@pytest.mark.asyncio
async def test_ensure_password_is_hashed(async_session: AsyncSession):
    repository = UserRepository(async_session)

    user = get_random_user()

    created_user = await repository.create_user(user)
    assert isinstance(created_user, User)

    assert created_user.password != user.password

    assert SecurityManager.verify_password(user.password, created_user.password)


@pytest.mark.asyncio
async def test_user_email_unique_constraint_in_create_and_update(async_session: AsyncSession):
    repository = UserRepository(async_session)

    original = get_random_user(dict(email='fazzuser@email.com'))
    same_email = get_random_user(dict(email='fazzuser@email.com'))

    original_user = await repository.create_user(original)

    # Update the user with the same email
    await repository.update_user_by_id(original_user.id, original)

    with pytest.raises(HTTPException, match='Email already in use'):
        await repository.create_user(same_email)

    some_user = get_random_user()
    created_user = await repository.create_user(some_user)

    some_user.email = original.email
    await repository.update_user_by_id(created_user.id, created_user)


def test_update_models_fields():
    from app.repository.shared_functions import update_model_fields

    user = get_random_user()
    user = User.model_validate(user)

    update_model_fields(user, dict(name='Fazz Name', email='fazzuser@email.com'))

    assert user.name == 'Fazz Name'
    assert user.email == 'fazzuser@email.com'
