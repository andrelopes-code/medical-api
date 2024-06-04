import debugpy
from fastapi import FastAPI
from app.core import settings
from app.api.v1.routers.configure import main_router

app = FastAPI(title='Medical Appointments', version='0.1.0')

if settings.DEBUG:
    debugpy.listen(('0.0.0.0', 5678))

app.include_router(main_router)
