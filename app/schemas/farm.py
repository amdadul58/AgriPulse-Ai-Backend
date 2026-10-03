from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class SoilType(str, Enum):
    clay = "clay"
    loam = "loam"
    sandy = "sandy"

class FarmCreate(BaseModel):
    name: str
    location: str
    soil_type: SoilType
    area_hectares: float

class FarmResponse(BaseModel):
    id: str
    name: str
    location: str
    soil_type: SoilType
    area_hectares: float
    created_at: datetime

    class Config:
        from_attributes = True
