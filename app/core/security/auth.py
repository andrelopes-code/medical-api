from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core import settings
from app.core.databases.postgres import sessionmaker
from app.core.exceptions import HttpExceptions
from app.core.security.security import SecurityService, TokenData, TokenResponse
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:

    async def login_user(self, email: str, password: str) -> dict:
        async with sessionmaker() as session:
            user_repository = UserRepository(session)

            # Check if user exists by email
            user = await user_repository.get_by_email(email)
            if not user:
                raise HttpExceptions.invalid_credentials()

            # Check if password is correct
            correct_password = SecurityService.verify_password(password, user.password)

            if not correct_password:
                raise HttpExceptions.invalid_credentials()

            # Create access token with user data and return it
            data_to_encode = TokenData(email=user.email, user_id=str(user.id), user_type=user.user_type.value)
            access_token = SecurityService.create_access_token(data_to_encode=data_to_encode)
            return TokenResponse(access_token=access_token, token_type='bearer')


# *** Security Dependencies ***

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.security.token_url)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    return SecurityService.verify_access_token(token)


async def get_current_db_user(user: Annotated[TokenData, Depends(get_current_user)]):
    async with sessionmaker() as session:
        user_repository = UserRepository(session)

        db_user = await user_repository.get_by_email(user['email'])
        if not db_user:
            raise HttpExceptions.invalid_credentials()

    return db_user


def get_current_admin_user(user: Annotated[TokenData, Depends(get_current_user)]):
    if user["user_type"] != "admin":
        raise HttpExceptions.invalid_credentials()
    return user


async def get_current_admin_db_user(user: Annotated[TokenData, Depends(get_current_admin_user)]):
    return await get_current_db_user(user)


DBAuthenticatedUserDepends = Annotated['User', Depends(get_current_db_user)]
AuthenticatedUserDepends = Depends(get_current_user)

DBAuthenticatedAdminUserDepends = Annotated['User', Depends(get_current_admin_db_user)]
AuthenticatedAdminUserDepends = Depends(get_current_admin_user)
