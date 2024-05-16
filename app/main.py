import logging
from fastapi import FastAPI

from app.logs import setup_logging
from app.routing import router, lifespan
from config.config import settings

logger = logging.getLogger(__name__)
setup_logging(settings.logging.level)

app = FastAPI(
    title=settings.openapi.title,
    description=settings.openapi.description,
    version=settings.openapi.version,
    lifespan=lifespan
)
app.include_router(router=router)
