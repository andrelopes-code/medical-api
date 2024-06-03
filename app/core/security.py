from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash

from app.core import settings
from app.core.exceptions import HttpExceptions

ALGORITHM = settings.security.algorithm
SECRET = settings.security.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.security.access_token_expire_minutes
pwd_context = PasswordHash.recommended()


class SecurityManager:

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

        except DecodeError:
            raise HttpExceptions.invalid_token()
        except Exception as e:
            raise HttpExceptions.internal_server_error(f'Error while decoding token: {e}')

    @staticmethod
    def get_password_hash(plain_password: str) -> str:
        hashed_password = pwd_context.hash(plain_password)
        return hashed_password

    @staticmethod
    def verify_password(password: str, hash: str) -> bool:
        is_valid = pwd_context.verify(password=password, hash=hash)
        return is_valid
