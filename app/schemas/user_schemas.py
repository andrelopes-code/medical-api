from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.types.user import UserGender, UserName, UserPassword, UserType


class UserInDB(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    password: str
    gender: UserGender
    user_type: UserType
    birthdate: datetime
    created_at: datetime
    updated_at: datetime


class UserCreateRequest(BaseModel):
    name: UserName
    email: EmailStr
    gender: UserGender
    phone: PhoneNumber
    password: UserPassword
    user_type: UserType
    birthdate: datetime


class UserCreateResponse(UserInDB):

    # * Excluded fields in the response
    password: str = Field(exclude=True)
    id: int = Field(exclude=True)


class UserUpdateRequest(BaseModel):
    name: UserName | None = None
    email: EmailStr | None = None
    phone: PhoneNumber | None = None
