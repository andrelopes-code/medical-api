from typing import Optional, Union

from sqlalchemy import exc
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import HttpExceptions, logger
from app.models.user import User
from app.schemas.user_schemas import UserCreateRequest, UserUpdateRequest

from . import shared_functions
from .shared_functions import handle_sqlalchemy_exception


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: Union[dict, UserCreateRequest]) -> Optional[User]:
        new_user = User.model_validate(user)
        await self._check_email_already_exists(new_user.email)
        try:
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return new_user

        except exc.SQLAlchemyError as e:
            logger.error('Error creating user: {}', e)

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        try:
            user = await self.session.get(User, user_id)
            return user
        except exc.SQLAlchemyError as e:
            logger.error('Error getting user: {}', e)

    async def get_user_by_email(self, email: str) -> Optional[User]: ...

    async def update_user_by_id(self, user_id: int, data: Union[dict, UserUpdateRequest]) -> Optional[User]:
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return None
            # Check if email is already in use and raise an error if it is
            email_in_update = self._get_field('email', data)
            if email_in_update and email_in_update != self._get_field('email', user):
                await self._check_email_already_exists(email_in_update)

            self._update_user_fields(user, data)

            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user

        except exc.SQLAlchemyError as e:
            logger.error('Error updating user: {}', e)

    async def update_user_by_email(self, email: str, data: Union[dict, UserUpdateRequest]) -> Optional[User]: ...

    async def delete_user_by_id(self, user_id: int) -> Optional[User]:
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return None

            await self.session.delete(user)
            await self.session.commit()
            return user
        except exc.SQLAlchemyError as e:
            logger.error('Error deleting user: {}', e)

    async def delete_user_by_email(self, email: str) -> Optional[User]: ...

    async def _check_email_already_exists(self, email: str) -> None:
        stmt = select(User).where(User.email == email)
        user = await self.session.scalar(stmt)
        if user:
            raise HttpExceptions.email_already_in_use()

    def _get_field(self, field_name: str, data: any):

        try:
            match data:
                case dict():
                    return data.get(field_name)
                case _:
                    return getattr(data, field_name)
        except Exception as e:
            logger.error('Error getting field: {}', e)

    def _update_user_fields(self, model: User, data: any):
        try:
            shared_functions.update_model_fields(model, data)
        except Exception as e:
            logger.error('Error updating user fields: {}', e)
            raise HttpExceptions.internal_server_error('Update operation failed')
