from enum import Enum

from pydantic_core import core_schema


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
