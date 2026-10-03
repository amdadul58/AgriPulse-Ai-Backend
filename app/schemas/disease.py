from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class DiseaseDetectionRequest(BaseModel):
    crop_name: str = Field(..., min_length=1)
    symptoms: str = Field(..., min_length=1)

    model_config = ConfigDict(str_strip_whitespace=True)


class TreatmentResponse(BaseModel):
    id: str
    recommendation_type: str
    description: str
    products: Optional[List[str]] = None
    dosage: Optional[str] = None
    application_method: Optional[str] = None
    precautions: Optional[str] = None


class DiseaseResponse(BaseModel):
    id: str
    name: str
    scientific_name: Optional[str] = None
    category: str
    symptoms: str
    causes: Optional[str] = None
    severity_level: str
    treatments: List[TreatmentResponse]

    model_config = ConfigDict(from_attributes=True)