from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID
from sqlalchemy import VARCHAR, DateTime, UUID as SaUUID
from sqlmodel import Field, Relationship, SQLModel

from app.models.utils import get_timestamp

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.appointment import Appointment


class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key='user.id', nullable=False, index=True, sa_type=SaUUID)
    created_at: datetime = Field(default_factory=get_timestamp, sa_type=DateTime(timezone=True), nullable=False)
    updated_at: datetime = Field(default_factory=get_timestamp, sa_type=DateTime(timezone=True), nullable=False)
    cpf: str = Field(nullable=False, unique=True, sa_type=VARCHAR(11))
    sus_card: str = Field(nullable=False, unique=True, sa_type=VARCHAR(15))

    user: Optional['User'] = Relationship(back_populates='patient')
    appointments: Optional[list['Appointment']] = Relationship(back_populates='doctor')
