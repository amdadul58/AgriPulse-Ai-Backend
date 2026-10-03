from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base
import uuid
class Treatment(Base):
    __tablename__ = 'treatments'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    disease_id = Column(String(36), ForeignKey('diseases.id', ondelete='CASCADE'), nullable=False)
    recommendation_type = Column(Enum('chemical', 'organic', 'cultural', name='treatment_types'), nullable=False)
    description = Column(Text, nullable=False)
    products = Column(JSON, nullable=True)
    dosage = Column(String(255), nullable=True)
    application_method = Column(Text, nullable=True)
    precautions = Column(Text, nullable=True)
    disease = relationship('Disease', back_populates='treatments')
