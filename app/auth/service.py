from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.security import get_password_hash, verify_password
import uuid
class AuthService:
    @staticmethod
    async def create_user(db: AsyncSession, email: str, full_name: str, password: str):
        user = User(id=str(uuid.uuid4()), email=email, full_name=full_name, hashed_password=get_password_hash(password))
        db.add(user); await db.commit(); await db.refresh(user); return user
    @staticmethod
    async def authenticate(db: AsyncSession, email: str, password: str):
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password): return None
        return user
