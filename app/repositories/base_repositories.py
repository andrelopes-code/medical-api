from typing import Optional, Sequence, Union
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import logger
from app.core.exceptions import UnexpectedError
from app.utils import functions


class BaseRepository[T]:
    """
    A repository class for basic database operations on any SQLModel model `T`.

    This class provides methods for creating, retrieving, updating, and deleting instances
    of a given model `T` using an asynchronous SQLAlchemy session. It is intended to be
    used as a base class for more specific repositories.

    Attributes:
        session (AsyncSession): The asynchronous SQLAlchemy session used for database operations.
        model (T): The SQLModel model class associated with this repository.

    Methods:
        create(instance: T) -> T:
            Adds a new instance of the model to the database and returns the created instance.

        get_all() -> Sequence[T]:
            Retrieves all instances of the model from the database and returns them as a list.

        get_by_id(pk: UUID) -> Optional[T]:
            Retrieves a single instance of the model by its primary key and returns it.

        delete_by_id(pk: UUID) -> Optional[T]:
            Deletes an instance of the model by its primary key and returns the deleted instance.

        update(instance: T, data: Union[dict, BaseModel]) -> T:
            Updates an instance of the model with the provided data and returns the updated instance.
    """

    def __init__(self, session: AsyncSession, model: 'T'):
        self.session = session
        self.model = model

    async def save(self, instance: 'T') -> 'T':
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_all(self) -> Sequence['T']:
        stmt = select(self.model)
        scalar_result = await self.session.scalars(stmt)
        instances = scalar_result.all()
        return instances

    async def get_by_id(self, pk: UUID | int) -> Optional['T']:
        return await self.session.get(self.model, pk)

    async def delete_by_id(self, pk: UUID | int) -> Optional['T']:
        instance = await self.get_by_id(pk)
        if not instance:
            return None

        await self.session.delete(instance)
        await self.session.commit()
        return instance

    async def update(self, instance: 'T', data: Union[dict, BaseModel]) -> 'T':
        return await self._update_instance(instance, data)

    async def _update_instance(self, instance: 'T', data: Union[dict, BaseModel]) -> 'T':
        self._update_instance_fields(instance, data)

        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    def _update_instance_fields(self, model: 'T', data: Union[dict, BaseModel]):
        try:
            functions.update_model_fields(model, data)
        except Exception as e:
            logger.exception(f'Error updating {self.model.__name__} fields: ')
            raise UnexpectedError(e)


class BaseRepositoryWithEmail[T](BaseRepository['T']):
    """
    A repository class for basic database operations on any SQLModel model `T` that includes email-based operations.

    This class extends the BaseRepository to add methods specifically for handling models that include an `email` field.
    It provides methods for retrieving and deleting instances by email address.

    Attributes:
        session (AsyncSession): The asynchronous SQLAlchemy session used for database operations.
        model (T): The SQLModel model class associated with this repository.

    Methods:
        get_by_email(email: str) -> Optional[T]:
            Retrieves a single instance of the model by its email and returns it.

        delete_by_email(email: str) -> Optional[T]:
            Deletes an instance of the model by its email and returns the deleted instance.

    Examples:
        class UserRepository(BaseRepositoryWithEmail[User]):
            def __init__(self, session: AsyncSession):
            super().__init__(session, User)
    """

    def __init__(self, session: AsyncSession, model: 'T'):
        super().__init__(session, model)

    async def get_by_email(self, email: str) -> Optional['T']:
        stmt = select(self.model).where(self.model.email == email)
        instance = await self.session.scalar(stmt)
        return instance

    async def delete_by_email(self, email: str) -> Optional['T']:
        instance = await self.get_by_email(email)
        if not instance:
            return None

        await self.session.delete(instance)
        await self.session.commit()
        return instance
