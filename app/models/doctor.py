from typing import TYPE_CHECKING, Optional
from uuid import UUID
from sqlalchemy import UUID as SaUUID, VARCHAR
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.appointment import Appointment


class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key='user.id', nullable=False, index=True, sa_type=SaUUID)
    crm: str = Field(nullable=False, index=True, sa_type=VARCHAR(255))
    specialty: str = Field(nullable=False, index=True, sa_type=VARCHAR(255))

    user: Optional['User'] = Relationship(back_populates='doctor')
    appointments: Optional[list['Appointment']] = Relationship(back_populates='doctor')
