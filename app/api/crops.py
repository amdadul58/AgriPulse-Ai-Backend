from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.farm import Farm
from app.models.crop import Crop
from app.schemas.crop import CropCreate, CropResponse
import uuid
router = APIRouter(prefix='/crops', tags=['Crops'])
@router.post('/', response_model=CropResponse)
async def add_crop(data: CropCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    farm = (await db.execute(select(Farm).where(Farm.id == data.farm_id))).scalar_one_or_none()
    if not farm or farm.user_id != current_user.id: raise HTTPException(status_code=403, detail='Not your farm')
    crop = Crop(id=str(uuid.uuid4()), **data.model_dump()); db.add(crop); await db.commit(); await db.refresh(crop); return crop
