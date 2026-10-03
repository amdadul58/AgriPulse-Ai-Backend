import httpx
from app.core.config import settings


class WeatherService:

    @staticmethod
    async def get_forecast(lat: float, lon: float):

        if not settings.WEATHER_API_KEY:
            return {
                "error": "Weather API key is not configured."
            }

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}"
            f"&lon={lon}"
            f"&appid={settings.WEATHER_API_KEY}"
            "&units=metric"
        )

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:

                response = await client.get(url)

                if response.status_code != 200:
                    return {
                        "error": "Weather API error",
                        "status_code": response.status_code
                    }

                data = response.json()

                return {
                    "city": data.get("name", "Unknown"),
                    "country": data.get("sys", {}).get("country", ""),
                    "temp": data.get("main", {}).get("temp"),
                    "feels_like": data.get("main", {}).get("feels_like"),
                    "humidity": data.get("main", {}).get("humidity"),
                    "pressure": data.get("main", {}).get("pressure"),
                    "wind_speed": data.get("wind", {}).get("speed"),
                    "description": (
                        data.get("weather", [{}])[0].get(
                            "description",
                            "Unknown"
                        )
                    ),
                    "icon": (
                        data.get("weather", [{}])[0].get(
                            "icon"
                        )
                    ),
                }

        except httpx.RequestError as e:

            return {
                "error": f"Weather service connection failed: {str(e)}"
            }

        except Exception as e:

            return {
                "error": f"Weather service error: {str(e)}"
            }