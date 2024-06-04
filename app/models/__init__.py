from sqlalchemy import event
from sqlmodel import SQLModel

from app.models.address import Address
from app.models.user import User
from app.models.utils import get_update_timestamp

event.listen(Address, 'before_update', get_update_timestamp)
event.listen(User, 'before_update', get_update_timestamp)
