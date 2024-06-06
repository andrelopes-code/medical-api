from datetime import datetime
from uuid import uuid4, UUID

from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy import VARCHAR, DateTime, UUID as SaUUID
from sqlmodel import Field, SQLModel

from app.models.utils import get_timestamp
from app.types.user import UserGender, UserHashedPassword, UserName, UserType


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, sa_type=SaUUID)
    name: UserName = Field(nullable=False, index=True, sa_type=VARCHAR(255))
    email: EmailStr = Field(nullable=False, unique=True, index=True, sa_type=VARCHAR(255))
    gender: UserGender = Field(nullable=False)
    password: UserHashedPassword = Field(nullable=False)
    birthdate: datetime = Field(sa_type=DateTime(timezone=True), nullable=False)
    user_type: UserType
    created_at: datetime = Field(default_factory=get_timestamp, sa_type=DateTime(timezone=True), nullable=False)
    updated_at: datetime = Field(default_factory=get_timestamp, sa_type=DateTime(timezone=True), nullable=False)
    phone: PhoneNumber
