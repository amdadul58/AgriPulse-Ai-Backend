from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database.base import Base
class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
