from logging import config as logging_config

from fastapi import FastAPI

from fastapi_service.api.v1 import model_server
from fastapi_service.settings.logger import LOGGING
from fastapi_service.settings.settings import settings

# from fastapi_service.model.model import Model
from fastapi_service.services.model_loader import get_transformer


app = FastAPI(
    title=settings.project.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)


@app.get("/")
async def root():
    return {"message": "good"}


@app.on_event("startup")
async def startup():
    #
    # Model().model = get_transformer()

    if settings.project.log_file:
        logging_config.dictConfig(LOGGING)


app.include_router(model_server.router, prefix="/api/v1/model_server", tags=["ml/dl"])
