from fastapi import FastAPI

from config.config import settings
from app.routing import router, lifespan


app = FastAPI(
    title=settings.openapi.title,
    description=settings.openapi.description,
    version=settings.openapi.version,
    lifespan=lifespan
)
app.include_router(router=router)
