from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base
import uuid
class Disease(Base):
    __tablename__ = 'diseases'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, unique=True)
    scientific_name = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True)
    symptoms = Column(Text, nullable=False)
    causes = Column(Text, nullable=True)
    affected_crops = Column(JSON, nullable=True)
    severity_level = Column(Enum('low', 'medium', 'high', 'critical', name='severity_levels'), default='medium')
    treatments = relationship('Treatment', back_populates='disease', cascade='all, delete-orphan')
