from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Log app startup and shutdown events."""
    logger.info("Application startup initiated")

    logger.info(
        "Configuration loaded: app_name=%s aws_region=%s",
        settings.app_name,
        settings.aws_region,
    )

    yield

    logger.info("Application shutdown initiated")