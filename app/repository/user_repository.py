from typing import Any, Optional, Sequence, Union
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import logger
from app.core.exceptions import UnexpectedError
from app.models.user import User
from app.schemas.user_schemas import UserUpdateRequest
from app.utils import functions


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, new_user: User) -> User:
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def get_all(self) -> Sequence[User]:
        stmt = select(User)
        result = await self.session.scalars(stmt)
        users = result.all()
        return users

    async def get_by_id(self, pk: UUID) -> Optional[User]:
        user = await self.session.get(User, pk)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        user = await self.session.scalar(stmt)
        return user

    async def update(self, user: User, data: Union[dict, UserUpdateRequest]) -> User:
        return await self._update_user(user, data)

    async def delete_by_id(self, pk: UUID) -> Optional[User]:
        user = await self.get_by_id(pk)
        if not user:
            return None

        return await self._delete_user(user)

    async def delete_by_email(self, email: str) -> Optional[User]:
        user = await self.get_by_email(email)
        if not user:
            return None

        return await self._delete_user(user)

    async def _delete_user(self, user: User) -> User:
        await self.session.delete(user)
        await self.session.commit()
        return user

    async def _update_user(self, user: User, data: Any) -> User:
        self._update_user_fields(user, data)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    def _get_field(self, field_name: str, data: Any):

        try:
            match data:
                case dict():
                    return data.get(field_name)
                case _:
                    return getattr(data, field_name)
        except Exception:
            logger.exception('Error getting field: ')

    def _update_user_fields(self, model: User, data: Any):
        try:
            functions.update_model_fields(model, data)
        except Exception as e:
            logger.error('Error updating user fields: {}', e)
            raise UnexpectedError(e)
