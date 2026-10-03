from fastapi import APIRouter

from app.api import (
    auth,
    farms,
    crops,
    diseases,
    chat,
    rag,
    vision,
    vector,
    health,
    weather,
    notifications,
    analytics,
)


api_router = APIRouter()


api_router.include_router(auth.router)
api_router.include_router(farms.router)
api_router.include_router(crops.router)
api_router.include_router(diseases.router)
api_router.include_router(chat.router)
api_router.include_router(rag.router)
api_router.include_router(vision.router)
api_router.include_router(vector.router)
api_router.include_router(health.router)
api_router.include_router(weather.router)
api_router.include_router(notifications.router)
api_router.include_router(analytics.router)

