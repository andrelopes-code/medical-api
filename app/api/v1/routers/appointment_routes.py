from uuid import UUID

from fastapi import APIRouter

from app.core.security.auth import AuthenticatedUserDepends
from app.schemas.appointment_schemas import AppointmentCreateRequest, AppointmentUpdateRequest
from app.services.appointment_service import AppointmentServiceDepends
from app.services.user_service import UserServiceDepends

router = APIRouter(dependencies=[AuthenticatedUserDepends])


@router.get('/appointment')
async def get_all_appointment(service: AppointmentServiceDepends):
    appointments = await service.get_all_appointments()
    return appointments


@router.get('/appointment/{appointment_id}')
async def get_appointment_by_id(service: AppointmentServiceDepends, appointment_id: int):
    appointment = await service.get_appointment_by_id(appointment_id)
    return appointment


@router.get('/appointment/user/{user_id}')
async def get_user_appointments(service: UserServiceDepends, user_id: UUID):
    user = await service.get_user_by_id(user_id)
    user_info = user.info
    if not user_info:
        return []

    appointments = await user_info.get_appointments()
    return appointments


@router.post('/appointment')
async def create_appointment(service: AppointmentServiceDepends, data: AppointmentCreateRequest):
    new_appointment = await service.create_appointment(data)
    return new_appointment


@router.patch('/appointment/{appointment_id}')
async def update_appointment_by_id(
    service: AppointmentServiceDepends, appointment_id: int, data: AppointmentUpdateRequest
):
    updated_appointment = await service.update_appointment_by_id(appointment_id, data)
    return updated_appointment


@router.delete('/appointment/{appointment_id}')
async def delete_appointment_by_id(service: AppointmentServiceDepends, appointment_id: int):
    deleted_appointment = await service.delete_appointment_by_id(appointment_id)
    return deleted_appointment
