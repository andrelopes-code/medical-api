from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import UUID as SaUUID, VARCHAR
from sqlmodel import Field, Relationship, SQLModel, select

from app.core.databases.postgres import sessionmaker

if TYPE_CHECKING:
    from app.models.appointment import Appointment
    from app.models.user import User


class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key='user.id', nullable=False, index=True, sa_type=SaUUID)
    crm: str = Field(nullable=False, index=True, sa_type=VARCHAR(255))
    specialty: str = Field(nullable=False, index=True, sa_type=VARCHAR(255))

    user: Optional['User'] = Relationship(back_populates='doctor', sa_relationship_kwargs={'lazy': 'selectin'})

    __appointments: Optional[list['Appointment']] = None

    async def get_appointments(self) -> list['Appointment']:
        if self.__appointments is None:
            from app.models.appointment import Appointment

            async with sessionmaker() as session:
                appointments = await session.scalars(select(Appointment).where(Appointment.doctor_id == self.id))
                self.__appointments = appointments.all()

        return self.__appointments
