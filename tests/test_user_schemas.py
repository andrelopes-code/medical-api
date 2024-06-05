import pytest
from util_functions import get_random_user

from app.models.user import User
from app.schemas.user_schemas import UserCreateRequest, UserCreateResponse, UserInDB, UserUpdateRequest


def test_user_schemas():
    user = get_random_user().model_dump()
    user.update(dict(id=8989))

    UserCreateRequest(**user)
    UserUpdateRequest(**user)
    response = UserCreateResponse(**user).model_dump()

    assert response.get('password') is None
    assert response.get('id') is None

    assert User.model_fields.keys() == UserInDB.model_fields.keys()
