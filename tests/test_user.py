from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


@pytest.mark.asyncio
async def test_user_updated_at_field_is_updating_correctly(async_session: AsyncSession):

    user = dict(
        name='John Doe',
        email='wYj5X@example.com',
        gender='male',
        birthdate=datetime.now(),
        phone='+5531988888888',
        user_type='patient',
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

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
