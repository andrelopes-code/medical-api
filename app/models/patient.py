from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import UUID as SaUUID, VARCHAR, DateTime
from sqlmodel import Field, Relationship, SQLModel, select

from app.core.databases.postgres import sessionmaker
from app.models.utils import get_timestamp

if TYPE_CHECKING:
    from app.models.appointment import Appointment
    from app.models.user import User


class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key='user.id', nullable=False, index=True, sa_type=SaUUID)
    created_at: datetime = Field(default_factory=get_timestamp, sa_type=DateTime(timezone=True), nullable=False)
    updated_at: datetime = Field(default_factory=get_timestamp, sa_type=DateTime(timezone=True), nullable=False)
    cpf: str = Field(nullable=False, unique=True, sa_type=VARCHAR(11))
    sus_card: str = Field(nullable=False, unique=True, sa_type=VARCHAR(15))

    user: Optional['User'] = Relationship(back_populates='patient', sa_relationship_kwargs={'lazy': 'selectin'})

    __appointments: Optional[list['Appointment']] = None

    async def get_appointments(self) -> list['Appointment']:
        if self.__appointments is None:
            from app.models.appointment import Appointment

            async with sessionmaker() as session:
                appointments = await session.scalars(select(Appointment).where(Appointment.patient_id == self.id))
                self.__appointments = appointments.all()

        return self.__appointments
