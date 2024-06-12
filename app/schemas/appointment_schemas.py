from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, Field


def min_appointment_date():
    return datetime.now(timezone.utc) + timedelta(minutes=60)


class AppointmentCreateRequest(BaseModel):
    doctor_id: int
    patient_id: int
    reason: str
    notes: str | None = None
    date: datetime = Field(gt=min_appointment_date())


class AppointmentUpdateRequest(BaseModel):
    reason: str
    notes: str | None = None
    date: datetime = Field(gt=min_appointment_date())


class AppointmentCreateResponse(AppointmentCreateRequest): ...
