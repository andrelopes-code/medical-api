from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.appointment import Appointment
from app.repositories.base_repositories import BaseRepository


class AppointmentRepository(BaseRepository[Appointment]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Appointment)
