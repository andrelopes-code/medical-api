from datetime import datetime
from typing import Optional

from sqlalchemy import TEXT, VARCHAR, DateTime
from sqlmodel import Field, Relationship, SQLModel

from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.utils import get_timestamp


class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    doctor_id: int = Field(foreign_key='doctor.id', nullable=False, index=True)
    patient_id: int = Field(foreign_key='patient.id', nullable=False, index=True)
    reason: str = Field(nullable=False, index=True, sa_type=VARCHAR(255))
    notes: Optional[str] = Field(nullable=True, sa_type=TEXT)
    date: datetime = Field(nullable=False, index=True, sa_type=DateTime(timezone=True))
    created_at: datetime = Field(default_factory=get_timestamp, sa_type=DateTime(timezone=True), nullable=False)
    updated_at: datetime = Field(default_factory=get_timestamp, sa_type=DateTime(timezone=True), nullable=False)

    doctor: Optional['Doctor'] = Relationship()
    patient: Optional['Patient'] = Relationship()
