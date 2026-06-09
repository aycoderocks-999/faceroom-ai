from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.routes import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging

settings = get_settings()
setup_logging()

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT])


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.DATABASE_URL.startswith("sqlite"):
        from app.core.database import Base, engine

        Base.metadata.create_all(bind=engine)
    try:
        from app.services.qdrant_service import QdrantService

        QdrantService().ensure_collection()
    except Exception:
        pass
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Distributed Face Recognition & Event Photo Retrieval Platform",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": f"{settings.API_PREFIX}/health",
    }
