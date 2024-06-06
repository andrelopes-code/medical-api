from typing import Annotated, Union

from fastapi import Depends
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.databases.postgres import AsyncDBSession
from app.core.exceptions import EmailAlreadyInUse, HttpExceptions
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.user_schemas import UserCreateRequest, UserUpdateRequest
from app.utils.decorators import handle_unexpected_exceptions


@handle_unexpected_exceptions()
class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UserRepository(session)

    async def create_user(self, user: Union[dict, UserCreateRequest]):
        try:
            new_user = User.model_validate(user)
            await self._check_email_already_exists(new_user.email)
            db_user = await self.repository.create_user(new_user)
            return db_user

        except EmailAlreadyInUse:
            raise HttpExceptions.email_already_in_use()

        except ValidationError as e:
            raise HttpExceptions.bad_request(e.errors())

    async def get_all_users(self):
        return await self.repository.get_all_users()

    async def get_user_by_id(self, user_id: int):
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise HttpExceptions.user_not_found()
        return user

    async def get_user_by_email(self, email: str):
        user = await self.repository.get_user_by_email(email)
        if not user:
            raise HttpExceptions.user_not_found()
        return user

    async def delete_user_by_id(self, user_id: int):
        user = await self.repository.delete_user_by_id(user_id)
        if not user:
            raise HttpExceptions.user_not_found()
        return user

    async def delete_user_by_email(self, email: str):
        user = await self.repository.delete_user_by_email(email)
        if not user:
            raise HttpExceptions.user_not_found()
        return user

    async def update_user_by_id(self, user_id: int, data: Union[dict, UserUpdateRequest]):
        try:
            user = await self.repository.get_user_by_id(user_id)
            if not user:
                raise HttpExceptions.user_not_found()

            email_in_update = self.repository._get_field('email', data)
            if email_in_update and email_in_update != self.repository._get_field('email', user):
                await self._check_email_already_exists(email_in_update)

            updated_user = await self.repository.update_user(user, data)
            return updated_user

        except EmailAlreadyInUse:
            raise HttpExceptions.email_already_in_use()

    async def update_user_by_email(self, email: str, data: Union[dict, UserUpdateRequest]):
        try:
            user = await self.repository.get_user_by_email(email)
            if not user:
                raise HttpExceptions.user_not_found()

            email_in_update = self.repository._get_field('email', data)
            if email_in_update and email_in_update != self.repository._get_field('email', user):
                await self._check_email_already_exists(email_in_update)

            updated_user = await self.repository.update_user(user, data)
            return updated_user

        except EmailAlreadyInUse:
            raise HttpExceptions.email_already_in_use()

    async def _check_email_already_exists(self, email: str) -> None:
        user = await self.repository.get_user_by_email(email)
        if user:
            raise EmailAlreadyInUse


# * Get User Service instance Dependency
def get_user_service(session: AsyncDBSession) -> UserService:
    return UserService(session)


GetUserService = Annotated[UserService, Depends(get_user_service)]
