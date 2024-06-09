from sqlalchemy import event
from sqlmodel import SQLModel

from app.models.address import Address
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.user import User
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.utils import get_update_timestamp

event.listen(Address, 'before_update', get_update_timestamp)
event.listen(User, 'before_update', get_update_timestamp)
event.listen(Appointment, 'before_update', get_update_timestamp)
