from fastapi import APIRouter, Depends
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import SecurityService

router = APIRouter()


@router.post('/token')
async def get_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    token = await SecurityService.login_user(email=form_data.username, password=form_data.password)
    return token
