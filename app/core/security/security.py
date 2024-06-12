from datetime import datetime, timedelta, timezone
from typing import TypedDict

from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash

from app.core import settings
from app.core.exceptions import HttpExceptions

ALGORITHM = settings.security.algorithm
SECRET = settings.security.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.security.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = settings.security.refresh_token_expire_minutes
PWD_CONTEXT = PasswordHash.recommended()


class TokenData(TypedDict):
    user_id: str
    email: str
    user_type: str


class TokenResponse(TypedDict):
    access_token: str
    refresh_token: str
    token_type: str


class SecurityService:
    """A class for handling security-related tasks, such as password hashing and token generation."""

    @staticmethod
    def _create_token(to_encode: dict) -> str:
        try:
            encoded_jwt = encode(payload=to_encode, algorithm=ALGORITHM, key=SECRET)
            return encoded_jwt

        except Exception as e:
            raise HttpExceptions.internal_server_error(f'Error while encoding token: {e}')

    @staticmethod
    def create_access_token(data_to_encode: dict) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = data_to_encode.copy()
        to_encode.update(dict(exp=expire, type='access'))
        access_token = SecurityService._create_token(to_encode=to_encode)
        return access_token

    @staticmethod
    def create_refresh_token(data_to_encode: dict) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode = data_to_encode.copy()
        to_encode.update(dict(exp=expire, type='refresh'))
        refresh_token = SecurityService._create_token(to_encode=to_encode)
        return refresh_token

    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            data = decode(jwt=token, key=SECRET, algorithms=[ALGORITHM])
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
