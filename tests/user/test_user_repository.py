from uuid import uuid4

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from util_functions import get_random_user

from app.core.security.security import SecurityService
from app.models.user import User
from app.repositories.user_repository import UserRepository


@pytest.mark.skip(reason='Needs to be fixed')
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


@pytest.mark.skip(reason='Needs to be fixed')
async def test_user_repository_create_user_and_get_user(async_session: AsyncSession):
    repository = UserRepository(async_session)

    random_user = get_random_user()
    user = User.model_validate(random_user)

    created_user = await repository.create(user)
    assert isinstance(created_user, User)

    db_user = await repository.get_by_id(created_user.id)
    assert db_user == created_user

    assert created_user.password != random_user.password


@pytest.mark.skip(reason='Needs to be fixed')
async def test_get_user_with_invalid_user_id(async_session: AsyncSession):
    repository = UserRepository(async_session)

    db_user = await repository.get_by_id(uuid4())
    assert db_user is None


@pytest.mark.skip(reason='Needs to be fixed')
async def test_update_user_with_valid_data(async_session: AsyncSession):
    repository = UserRepository(async_session)

    random_user = get_random_user()
    user = User.model_validate(random_user)

    created_user = await repository.create(user)
    assert isinstance(created_user, User)

    updates = [
        dict(name='Fazz Name', email='fazzuser@email.com'),
        dict(gender='other', phone='+5521977776666'),
        dict(
            name='Bar Name Name',
            email='barbar@outlook.com',
            gender='female',
            user_type='doctor',
        ),
    ]

    for update_data in updates:
        updated_user = await repository.update(created_user, update_data)

        for field, value in update_data.items():
            if value is not None:
                assert getattr(updated_user, field) == value


@pytest.mark.skip(reason='Needs to be fixed')
async def test_delete_user_by_id(async_session: AsyncSession):
    repository = UserRepository(async_session)

    user = get_random_user()

    fake_user = await repository.delete_by_id(uuid4())
    assert fake_user is None

    created_user = await repository.create(user)
    assert isinstance(created_user, User)

    deleted_user = await repository.delete_by_id(created_user.id)
    assert deleted_user == created_user

    db_user = await repository.get_by_id(created_user.id)
    assert db_user is None


@pytest.mark.skip(reason='Needs to be fixed')
async def test_ensure_password_is_hashed(async_session: AsyncSession):
    repository = UserRepository(async_session)

    random_user = get_random_user()
    user = User.model_validate(random_user)

    created_user = await repository.create(user)
    assert isinstance(created_user, User)

    assert created_user.password != random_user.password

    assert SecurityService.verify_password(random_user.password, created_user.password)


@pytest.mark.skip(reason='Needs to be fixed')
async def test_get_user_by_email(async_session: AsyncSession):
    repository = UserRepository(async_session)

    user = get_random_user()
    created_user = await repository.create(user)
    assert isinstance(created_user, User)

    db_user = await repository.get_by_email(created_user.email)
    assert db_user == created_user


@pytest.mark.skip(reason='Needs to be fixed')
async def test_delete_user_by_email(async_session: AsyncSession):
    repository = UserRepository(async_session)

    user = get_random_user()
    created_user = await repository.create(user)
    assert isinstance(created_user, User)

    db_user = await repository.delete_by_email(created_user.email)
    assert db_user == created_user

    no_user = await repository.get_by_email(created_user.email)
    assert no_user is None


@pytest.mark.skip(reason='Needs to be fixed')
async def test_get_all_users(async_session: AsyncSession):
    repository = UserRepository(async_session)

    users = [get_random_user() for _ in range(10)]

    for user in users:
        await repository.create(user)

    db_users = await repository.get_all()
    assert len(db_users) == len(users)


@pytest.mark.skip(reason='Needs to be fixed')
def test_update_models_fields():
    from app.utils.functions import update_model_fields

    user = get_random_user()
    user = User.model_validate(user)

    update_model_fields(user, dict(name='Fazz Name', email='fazzuser@email.com'))

    assert user.name == 'Fazz Name'
    assert user.email == 'fazzuser@email.com'
