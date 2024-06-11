from typing import Union

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.address import Address
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.user import User
from app.repositories.base_repositories import BaseRepository, BaseRepositoryWithEmail


class UserRepository(BaseRepositoryWithEmail[User]):
    """A repository class for basic database operations on `User` instances"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def create(self, user: User, user_type: Union[Doctor, Patient]):
        self.session.add(user)
        self.session.add(user_type)
        await self.session.commit()
        await self.session.refresh(user)
        return user


class AddressRepository(BaseRepository[Address]):
    """A repository class for basic database operations on `Address` instances"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Address)
