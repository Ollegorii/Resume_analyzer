import uvicorn

from fastapi_service import app
from fastapi_service.settings.settings import settings

uvicorn.run(app, host=settings.api.host, port=int(settings.api.port))
