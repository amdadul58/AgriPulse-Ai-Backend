from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.repositories.farm_repository import FarmRepository
from app.schemas.farm import FarmCreate, FarmResponse
import uuid
router = APIRouter(prefix='/farms', tags=['Farms'])
@router.post('/', response_model=FarmResponse)
async def create_farm(data: FarmCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = FarmRepository(db); return await repo.create(id=str(uuid.uuid4()), user_id=current_user.id, **data.model_dump())
@router.get('/', response_model=list[FarmResponse])
async def get_farms(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = FarmRepository(db); return await repo.get_by_user_id(current_user.id)
