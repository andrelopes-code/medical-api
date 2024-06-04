from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import VARCHAR
from sqlmodel import Field, SQLModel

from app.types.address import AddressCep, AddressFormated, AddressNumber, AddressState


class Address(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id', nullable=False, index=True)
    city: AddressFormated = Field(nullable=False, index=True, sa_type=VARCHAR(255))
    street: AddressFormated = Field(nullable=False, index=True, sa_type=VARCHAR(255))
    number: AddressNumber = Field(nullable=False, index=True, sa_type=VARCHAR(10))
    state: AddressState = Field(nullable=False, index=True, sa_type=VARCHAR(2))
    cep: AddressCep = Field(nullable=False, index=True, sa_type=VARCHAR(9))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)