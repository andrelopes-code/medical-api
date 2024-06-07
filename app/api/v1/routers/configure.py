from fastapi import APIRouter

from app.api.v1.routers.user_routes import router as user_router
from app.api.v1.routers.token_routes import router as token_router

main_router = APIRouter(prefix='/api/v1')


# Configure the sub-routers
main_router.include_router(user_router, tags=['User'])
main_router.include_router(token_router, tags=['Token'])
