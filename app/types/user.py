from enum import Enum

from pydantic_core import core_schema

from app.core import logger
from app.core.security import SecurityManager


class UserType(str, Enum):
    patient = 'patient'
    doctor = 'doctor'
    admin = 'admin'


class UserGender(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'


class UserName(str):

    def __init__(self, name) -> None:
        splited = name.split(' ')
        self.first = splited[0]
        self.last = ' '.join(splited[1:])

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source,
        _handler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(cls._validate, core_schema.str_schema())

    @classmethod
    def _validate(cls, name: str, /) -> str:
        import re

        name_striped = re.sub(r'\s+', ' ', name.strip().title())
        return cls(name_striped)


class UserHashedPassword(str):

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source,
        _handler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(cls._validate, core_schema.str_schema())

    @classmethod
    def _validate(cls, password: str, /) -> str:

        try:
            hashed_password = SecurityManager.get_password_hash(password)
            return cls(hashed_password)
        except Exception as e:
            logger.debug('Error hashing password: {}', e)


class UserPassword(str):

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source,
        _handler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(cls._validate, core_schema.str_schema())

    @classmethod
    def _validate(cls, password: str, /) -> str:
        import re

        password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&_])[A-Za-z\d$@$!%*?&_]{8,40}$')
        is_valid = password_pattern.match(password)
        if not is_valid:
            raise ValueError(
                'Password must have at least 8 characters (max 40), 1 uppercase, 1 lowercase, 1 number and 1 special character'
            )

        return cls(password)
