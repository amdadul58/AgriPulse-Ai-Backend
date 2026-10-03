from pydantic import BaseModel
from datetime import date, datetime

class CropCreate(BaseModel):
    farm_id: str
    name: str
    variety: str | None = None
    planting_date: date

class CropResponse(BaseModel):
    id: str
    farm_id: str
    name: str
    variety: str | None
    planting_date: date
    health_status: str
    created_at: datetime

    class Config:
        from_attributes = True
