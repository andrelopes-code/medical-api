from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.appointment import Appointment
from app.repositories.base_repositories import BaseRepository


class AppointmentRepository(BaseRepository[Appointment]):
    """A repository class for basic database operations on `Appointment` instances"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Appointment)
