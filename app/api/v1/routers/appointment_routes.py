from fastapi import APIRouter

from app.schemas.appointment_schemas import AppointmentCreateRequest
from app.services.appointment_service import AppointmentServiceDepends

router = APIRouter()


@router.post('/appointment')
async def create_appointment(service: AppointmentServiceDepends, data: AppointmentCreateRequest):
    new_appointment = await service.create_appointment(data)
    return new_appointment
