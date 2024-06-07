from datetime import datetime, timedelta
from typing import Annotated, TypedDict
import typing
from zoneinfo import ZoneInfo

from fastapi import Depends
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash

from app.core import settings
from app.core.exceptions import HttpExceptions
from fastapi.security import OAuth2PasswordBearer
from app.core.databases.postgres import sessionmaker
from app.services.user_service import UserService

if typing.TYPE_CHECKING:
    from app.models.user import User

ALGORITHM = settings.security.algorithm
SECRET = settings.security.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.security.access_token_expire_minutes
PWD_CONTEXT = PasswordHash.recommended()


class TokenData(TypedDict):
    user_id: str
    username: str
    email: str


class TokenResponse(TypedDict):
    access_token: str
    token_type: str


class SecurityService:

    @staticmethod
    def create_access_token(data_to_encode: dict) -> str:

        to_encode = data_to_encode.copy()
        expire = datetime.now(ZoneInfo('UTC')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update(dict(exp=expire))

        try:
            encoded_jwt = encode(payload=to_encode, algorithm=ALGORITHM, key=SECRET)
            return encoded_jwt

        except Exception as e:
            raise HttpExceptions.internal_server_error(f'Error while encoding token: {e}')

    @staticmethod
    def verify_access_token(access_token: str) -> dict:
        try:
            data = decode(jwt=access_token, key=SECRET, algorithms=[ALGORITHM])
            return data

        except (DecodeError, ExpiredSignatureError):
            raise HttpExceptions.invalid_token()

    @staticmethod
    def get_password_hash(plain_password: str) -> str:
        hashed_password = PWD_CONTEXT.hash(plain_password)
        return hashed_password

    @staticmethod
    def verify_password(password: str, hash: str) -> bool:
        is_valid = PWD_CONTEXT.verify(password=password, hash=hash)
        return is_valid

    @staticmethod
    async def login_user(email: str, password: str) -> dict:
        async with sessionmaker() as session:
            user_service = UserService(session)
            user = await user_service.get_user_by_email(email)
            valid_password = SecurityService.verify_password(password, user.password)

            if not valid_password:
                raise HttpExceptions.invalid_credentials()

            data_to_encode = TokenData(email=user.email, user_id=str(user.id), user_type=user.user_type)

            access_token = SecurityService.create_access_token(data_to_encode=data_to_encode)
            return TokenResponse(access_token=access_token, token_type='bearer')


"""Security Dependencies"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.security.token_url)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    return SecurityService.verify_access_token(token)


async def get_current_db_user(user: Annotated[TokenData, Depends(get_current_user)]):
    async with sessionmaker() as session:
        user_service = UserService(session)
        db_user = await user_service.get_user_by_email(user.email)
    return db_user


AuthenticatedDBUserDepends = Annotated['User', Depends(get_current_db_user)]
AuthenticatedUserDepends = Depends(get_current_user)
