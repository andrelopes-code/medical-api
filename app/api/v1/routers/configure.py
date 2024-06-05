from fastapi import APIRouter

from .user_routes import user_router

main_router = APIRouter(prefix='/api/v1')


# Configure the sub-routers
main_router.include_router(user_router, tags=['User'])
