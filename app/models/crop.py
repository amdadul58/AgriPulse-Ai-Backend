from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base
import uuid
class Crop(Base):
    __tablename__ = 'crops'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    farm_id = Column(String(36), ForeignKey('farms.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    variety = Column(String(255), nullable=True)
    planting_date = Column(Date, nullable=False)
    health_status = Column(Enum('healthy', 'warning', 'diseased', name='health_statuses'), default='healthy')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    farm = relationship('Farm', back_populates='crops')
