from fastapi import APIRouter, Depends, Query
from app.dependencies import get_current_user
from app.models.user import User
from app.services.weather.weather_service import WeatherService


router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)


@router.get("/")
async def get_weather(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    current_user: User = Depends(get_current_user)
):
    return await WeatherService.get_forecast(lat, lon)