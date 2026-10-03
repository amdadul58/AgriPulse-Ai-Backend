from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.farm import Farm
from app.repositories.base_repository import BaseRepository
class FarmRepository(BaseRepository):
    def __init__(self, db: AsyncSession): super().__init__(db, Farm)
    async def get_by_user_id(self, user_id: str):
        result = await self.db.execute(select(Farm).where(Farm.user_id == user_id)); return result.scalars().all()
