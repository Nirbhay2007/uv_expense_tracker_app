from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.expense import router as expense_router
from app.core.config import settings
from app.core.logger import bootstrap_logging, get_logger
from app.lifecycle import lifespan

bootstrap_logging(settings.log_level)

logger = get_logger(__name__)

logger.info("Application bootstrap started")

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/")
async def root():
    return {
        "app": settings.app_name,
        "version": "0.1.0",
        "status": "running",
    }

app.include_router(health_router)
app.include_router(expense_router)

logger.info(
    "Application context loaded: app_name=%s aws_region=%s",
    settings.app_name,
    settings.aws_region,
)

logger.info(
    "Application ready: log_level=%s",
    settings.log_level,
)

logger.info("Application bootstrap completed successfully")