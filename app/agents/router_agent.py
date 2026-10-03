from app.services.vision.disease_detector import DiseaseDetector
from app.services.ai.chat_service import ChatService
from app.services.weather.weather_service import WeatherService

class RouterAgent:
    @staticmethod
    async def process_input(query: str, db, image_base64: str = None):
        # Weather check
        if 'weather' in query.lower():
            weather = await WeatherService.get_forecast(23.7, 90.3)
            return f'🌤️ Weather: {weather}', 'weather'
        
        # Vision check
        if image_base64:
            result = await DiseaseDetector.detect(image_base64)
            return f'🖼️ Image Analysis: {result.get("detected_disease")}', 'vision'
        
        # Text chat
        reply, source = await ChatService.handle_text(query, db)
        return reply, source
