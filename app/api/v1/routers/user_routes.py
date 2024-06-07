from uuid import UUID

from fastapi import APIRouter, status

from app.schemas.user_schemas import UserCreateRequest, UserResponseDefault, UserUpdateRequest
from app.services.user_service import UserServiceDepends


from app.core.security import AuthenticatedUserDepends

router = APIRouter(dependencies=[AuthenticatedUserDepends])


@router.post('/user', response_model=UserResponseDefault, status_code=status.HTTP_201_CREATED)
async def create_user(service: UserServiceDepends, user: UserCreateRequest):
    created_user = await service.create_user(user)
    return created_user


@router.get('/user', response_model=list[UserResponseDefault])
async def get_users(service: UserServiceDepends):
    users = await service.get_all_users()
    return users


@router.get('/user/{user_id}', response_model=UserResponseDefault)
async def get_user_by_id(service: UserServiceDepends, user_id: UUID):
    users = await service.get_user_by_id(user_id)
    return users


@router.patch('/user/{user_id}', response_model=UserResponseDefault)
async def update_user(service: UserServiceDepends, update_data: UserUpdateRequest, user_id: UUID):
    updated_user = await service.update_user_by_id(user_id, update_data)
    return updated_user
