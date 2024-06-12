from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.types.user import UserGender, UserName, UserPassword, UserType


class UserInDB(BaseModel):
    id: UUID
    name: str
    email: str
    phone: str
    password: str
    gender: UserGender
    user_type: UserType
    birthdate: datetime
    created_at: datetime
    updated_at: datetime
    is_deleted: bool


class UserUpdateRequest(BaseModel):
    name: UserName | None = None
    email: EmailStr | None = None
    phone: PhoneNumber | None = None


class DoctorCreate(BaseModel):
    specialty: str = Field(max_length=255)
    crm: str = Field(pattern=r'^\d{6}-\d{2}\/[A-Z]{2}$')


class DoctorResponse(BaseModel):
    id: int
    crm: str
    specialty: str


class PatientCreate(BaseModel):
    cpf: str = Field(pattern=r'[0-9]{11}')
    sus_card: str = Field(pattern=r'[0-9]{15}')


class PatientResponse(BaseModel):
    id: int
    cpf: str
    sus_card: str


class UserCreate(BaseModel):
    name: UserName
    email: EmailStr
    gender: UserGender
    phone: PhoneNumber
    password: UserPassword
    user_type: UserType
    birthdate: datetime


class UserCreateRequest(BaseModel):
    user: UserCreate
    doctor: Optional[DoctorCreate] = None
    patient: Optional[PatientCreate] = None


class UserResponseDefault(UserInDB):

    # * Excluded fields in the response
    password: str = Field(exclude=True)

    doctor: Optional[DoctorResponse] = None
    patient: Optional[PatientResponse] = None
