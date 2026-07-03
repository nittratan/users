import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import configure_logging
from app.middleware.request_logging import request_logging_middleware


configure_logging()
logger = logging.getLogger("user_api")


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("User API started")
    yield
    logger.info("User API stopped")


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )
    application.middleware("http")(request_logging_middleware)
    register_exception_handlers(application)
    application.include_router(api_router)
    return application


app = create_app()

