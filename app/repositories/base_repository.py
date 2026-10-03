from sqlalchemy.ext.asyncio import AsyncSession
class BaseRepository:
    def __init__(self, db: AsyncSession, model): self.db = db; self.model = model
    async def create(self, **kwargs):
        instance = self.model(**kwargs); self.db.add(instance); await self.db.commit(); await self.db.refresh(instance); return instance
