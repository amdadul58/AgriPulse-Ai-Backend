from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.notification import Notification

from app.schemas.disease import (
    DiseaseDetectionRequest,
    DiseaseResponse,
    TreatmentResponse
)

from app.services.recommendation.crop_recommendation import (
    CropAdvisorService
)


router = APIRouter(
    prefix="/diseases",
    tags=["Diseases"]
)


@router.post(
    "/detect",
    response_model=DiseaseResponse
)
async def detect_disease(
    req: DiseaseDetectionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Detect crop disease from crop name and symptoms.

    Flow:
    1. Generate embedding
    2. Search Chroma
    3. Find disease in PostgreSQL
    4. Find treatments in PostgreSQL
    5. Create automatic notification
    6. Return DiseaseResponse
    """

    # ------------------------------------------------------
    # Disease Detection
    # ------------------------------------------------------

    result = await CropAdvisorService.detect_disease_and_suggest(
        db=db,
        crop_name=req.crop_name,
        symptoms=req.symptoms
    )

    # ------------------------------------------------------
    # Disease not found
    # ------------------------------------------------------

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Disease not found"
        )

    # ------------------------------------------------------
    # Service returns:
    #
    # (disease, treatments)
    # ------------------------------------------------------

    disease, treatments = result

    # ------------------------------------------------------
    # Create Automatic Disease Notification
    # ------------------------------------------------------

    severity = (
        str(disease.severity_level)
        if disease.severity_level
        else "medium"
    )

    notification = Notification(
        user_id=current_user.id,
        title=f"{req.crop_name} Disease Detected",
        message=(
            f"{disease.name} has been detected in your "
            f"{req.crop_name} crop based on the provided symptoms. "
            f"Severity level: {severity}. "
            f"Please review the recommended treatments."
        ),
        type="disease",
        is_read=False
    )

    db.add(notification)

    # ------------------------------------------------------
    # Build TreatmentResponse list
    # ------------------------------------------------------

    treatment_responses = [
        TreatmentResponse(
            id=str(t.id),
            recommendation_type=t.recommendation_type,
            description=t.description,
            products=t.products,
            dosage=t.dosage,
            application_method=t.application_method,
            precautions=t.precautions
        )
        for t in treatments
    ]

    # ------------------------------------------------------
    # Save notification + changes
    # ------------------------------------------------------

    await db.commit()

    # ------------------------------------------------------
    # Return DiseaseResponse
    # ------------------------------------------------------

    return DiseaseResponse(
        id=str(disease.id),
        name=disease.name,
        scientific_name=disease.scientific_name,
        category=disease.category,
        symptoms=disease.symptoms,
        causes=disease.causes,
        severity_level=disease.severity_level,
        treatments=treatment_responses
    )

