from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import UUID as SaUUID, VARCHAR, DateTime
from sqlmodel import Field, Relationship, SQLModel

from app.models.user import User
from app.types.address import AddressCep, AddressFormated, AddressNumber, AddressState


class Address(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key='user.id', nullable=False, index=True, sa_type=SaUUID)
    city: AddressFormated = Field(nullable=False, index=True, sa_type=VARCHAR(255))
    street: AddressFormated = Field(nullable=False, index=True, sa_type=VARCHAR(255))
    number: AddressNumber = Field(nullable=False, index=True, sa_type=VARCHAR(10))
    state: AddressState = Field(nullable=False, index=True, sa_type=VARCHAR(2))
    cep: AddressCep = Field(nullable=False, index=True, sa_type=VARCHAR(9))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime(timezone=True), nullable=False
    )
    is_deleted: bool = Field(default=False, nullable=False, index=True)

    user: Optional['User'] = Relationship(back_populates='address')
