from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.vision.disease_detector import DiseaseDetector
import base64

router = APIRouter(prefix='/vision', tags=['Vision'])

@router.post('/detect')
async def detect_disease_from_image(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    ছবি আপলোড করে রোগ শনাক্ত করে (Vision AI)।
    """
    try:
        content = await image.read()
        image_b64 = base64.b64encode(content).decode('utf-8')
        image_b64 = f"data:image/jpeg;base64,{image_b64}"
        
        result = await DiseaseDetector.detect(image_b64)
        return result
    except Exception as e:
        return {"error": str(e), "detected_disease": "Unknown"}
