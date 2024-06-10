from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union
from uuid import UUID, uuid4

from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy import UUID as SaUUID, VARCHAR, DateTime
from sqlmodel import Field, Relationship, SQLModel

from app.models.utils import get_timestamp
from app.types.user import UserGender, UserHashedPassword, UserName, UserType

if TYPE_CHECKING:
    from app.models.address import Address
    from app.models.doctor import Doctor
    from app.models.patient import Patient


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

    doctor: Optional['Doctor'] = Relationship(back_populates='user')
    patient: Optional['Patient'] = Relationship(back_populates='user')
    address: Optional['Address'] = Relationship(back_populates='user')

    @property
    def info(self) -> Union['Doctor', 'Patient']:
        if self.user_type == UserType.doctor:
            return self.doctor
        elif self.user_type == UserType.patient:
            return self.patient
