from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.address import Address
from app.models.user import User
from app.repository.base_repositories import BaseRepository, BaseRepositoryWithEmail


class UserRepository(BaseRepositoryWithEmail[User]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, User)


class AddressRepository(BaseRepository[Address]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Address)
