from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database.session import get_db

router = APIRouter(prefix='/health', tags=['Health'])

@router.get('/')
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # SQLAlchemy 2.0-তে text() ব্যবহার করতে হবে
        await db.execute(text('SELECT 1'))
        return {
            'status': 'healthy', 
            'database': 'connected', 
            'service': 'AgriPulse-Ai'
        }
    except Exception as e:
        return {
            'status': 'unhealthy', 
            'database': str(e), 
            'service': 'AgriPulse-Ai'
        }
