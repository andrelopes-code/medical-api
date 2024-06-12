from fastapi import APIRouter

from app.api.v1.routers.appointment_routes import router as appointment_router
from app.api.v1.routers.token_routes import router as token_router
from app.api.v1.routers.user_routes import router as user_router

main_router = APIRouter(prefix='/api/v1')


# Configure the sub-routers
main_router.include_router(user_router, tags=['User'])
main_router.include_router(token_router, tags=['Auth'])
main_router.include_router(appointment_router, tags=['Appointment'])
