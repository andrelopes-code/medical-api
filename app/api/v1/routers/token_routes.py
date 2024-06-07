from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security.auth import AuthService
from app.core.security.security import TokenResponse

router = APIRouter()

auth_service = AuthService()


@router.post('/token')
async def get_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenResponse:
    token = await auth_service.login_user(email=form_data.username, password=form_data.password)
    return token
