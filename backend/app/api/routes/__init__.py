from fastapi import APIRouter

from app.api.routes import auth, clusters, dashboard, images, rooms, search, system

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(rooms.router, prefix="/rooms", tags=["Rooms"])
api_router.include_router(images.router, prefix="/images", tags=["Images"])
api_router.include_router(clusters.router, prefix="/clusters", tags=["Clusters"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(system.router, tags=["System"])
