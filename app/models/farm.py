from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base
import uuid
class Farm(Base):
    __tablename__ = 'farms'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    soil_type = Column(Enum('clay', 'loam', 'sandy', name='soil_types'), nullable=False)
    area_hectares = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    crops = relationship('Crop', back_populates='farm', cascade='all, delete-orphan')
