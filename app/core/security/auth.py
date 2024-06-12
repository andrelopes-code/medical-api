from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer

from app.core import settings
from app.core.databases.postgres import sessionmaker
from app.core.exceptions import HttpExceptions
from app.core.security.security import SecurityService, TokenData, TokenResponse
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:

    @staticmethod
    async def login_user(email: str, password: str) -> dict:
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

            # Create access token and refresh token with user data and return it
            data_to_encode = TokenData(email=user.email, user_id=str(user.id), user_type=user.user_type.value)
            return AuthService.create_access_and_refresh_token(data_to_encode=data_to_encode)

    @staticmethod
    def refresh_token(request: Request) -> TokenResponse:

        # Get the refresh token from the Authorization header
        refresh_token = request.headers.get('Authorization')
        if not refresh_token:
            raise HttpExceptions.bad_request('Missing refresh token')

        # Try to decode the refresh token
        token_data = SecurityService.verify_token(refresh_token.removeprefix('Bearer '))

        # Ensure that the token type is refresh
        if token_data['type'] != 'refresh':
            raise HttpExceptions.bad_request('Invalid refresh token')

        # Create new access and refresh tokens with the same user data and return them
        tokens = AuthService.create_access_and_refresh_token(data_to_encode=token_data)
        return tokens

    @staticmethod
    def create_access_and_refresh_token(data_to_encode: TokenData) -> TokenResponse:
        access_token = SecurityService.create_access_token(data_to_encode=data_to_encode)
        refresh_token = SecurityService.create_refresh_token(data_to_encode=data_to_encode)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token, token_type='Bearer')


# *** Security Dependencies ***

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.security.token_url)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    return SecurityService.verify_token(token)


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
