import debugpy
from fastapi import FastAPI

from app.api.v1.routers.configure import main_router
from app.core import settings
from app.core.middlewares import configure_cors

app = FastAPI(title='Medical Appointments', version='0.1.0')
configure_cors(app)

if settings.DEBUG:
    debugpy.listen(('0.0.0.0', 5678))

app.include_router(main_router)
