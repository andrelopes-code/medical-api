from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy import VARCHAR
from sqlmodel import Field, SQLModel

from app.models.utils import get_timestamp
from app.types.user import UserGender, UserName, UserType, UserHashedPassword


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: UserName = Field(nullable=False, index=True, sa_type=VARCHAR(255))
    email: EmailStr = Field(nullable=False, unique=True, index=True, sa_type=VARCHAR(255))
    gender: UserGender = Field(nullable=False)
    hashed_password: UserHashedPassword = Field(nullable=False)
    birthdate: datetime
    user_type: UserType
    created_at: datetime = Field(default_factory=get_timestamp, nullable=False)
    updated_at: datetime = Field(default_factory=get_timestamp, nullable=False)
    phone: PhoneNumber
