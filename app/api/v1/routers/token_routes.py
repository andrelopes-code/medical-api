from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security.auth import AuthService
from app.core.security.security import TokenResponse

router = APIRouter()


@router.post('/token')
async def get_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenResponse:
    tokens = await AuthService.login_user(email=form_data.username, password=form_data.password)
    return tokens


@router.post('/token/refresh')
async def refresh_access_token(request: Request):
    new_tokens = AuthService.refresh_token(request=request)
    return new_tokens
