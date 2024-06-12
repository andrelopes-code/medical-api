from typing import Annotated

from fastapi import Depends
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.databases.postgres import AsyncSessionDepends
from app.core.exceptions import HttpExceptions
from app.models.appointment import Appointment
from app.repositories.appointment_repository import AppointmentRepository
from app.schemas.appointment_schemas import AppointmentCreateRequest, AppointmentUpdateRequest


class AppointmentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = AppointmentRepository(session)

    async def create_appointment(self, data: AppointmentCreateRequest):
        try:
            appointment = Appointment.model_validate(data)
            db_appointment = await self.repository.save(appointment)
            return db_appointment

        except ValidationError as e:
            raise HttpExceptions.bad_request(e.errors())

    async def get_all_appointments(self):
        return await self.repository.get_all()

    async def get_appointment_by_id(self, appo_id: int):
        return await self.repository.get_by_id(appo_id)

    async def update_appointment_by_id(self, appo_id: int, data: AppointmentUpdateRequest):
        appointment = self.get_appointment_by_id(appo_id)
        if not appointment:
            raise HttpExceptions.not_found('Appointment not found')

        updated_appointment = await self.repository.update(appointment, data)

        return updated_appointment

    async def delete_appointment_by_id(self, appo_id: int):
        deleted_appointment = await self.repository.delete_by_id(appo_id)
        if not deleted_appointment:
            raise HttpExceptions.not_found('Appointment not found')

        return deleted_appointment


# * Get Appointment Service instance Dependency
async def get_appointment_service(session: AsyncSessionDepends):
    return AppointmentService(session)


AppointmentServiceDepends = Annotated[AppointmentService, Depends(get_appointment_service)]
