from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.farm import Farm
from app.models.crop import Crop
from app.models.disease import Disease


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/summary")
async def analytics_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Return analytics summary for the current user's agriculture data.
    """

    # -----------------------------------------
    # Total farms for current user
    # -----------------------------------------
    farms_result = await db.execute(
        select(func.count(Farm.id)).where(
            Farm.user_id == current_user.id
        )
    )

    total_farms = farms_result.scalar() or 0

    # -----------------------------------------
    # Total crops for current user's farms
    # -----------------------------------------
    crops_result = await db.execute(
        select(func.count(Crop.id))
        .join(Farm, Crop.farm_id == Farm.id)
        .where(Farm.user_id == current_user.id)
    )

    total_crops = crops_result.scalar() or 0

    # -----------------------------------------
    # Crop health status
    # -----------------------------------------
    healthy_result = await db.execute(
        select(func.count(Crop.id))
        .join(Farm, Crop.farm_id == Farm.id)
        .where(
            Farm.user_id == current_user.id,
            Crop.health_status == "healthy",
        )
    )

    healthy_crops = healthy_result.scalar() or 0

    warning_result = await db.execute(
        select(func.count(Crop.id))
        .join(Farm, Crop.farm_id == Farm.id)
        .where(
            Farm.user_id == current_user.id,
            Crop.health_status == "warning",
        )
    )

    warning_crops = warning_result.scalar() or 0

    diseased_result = await db.execute(
        select(func.count(Crop.id))
        .join(Farm, Crop.farm_id == Farm.id)
        .where(
            Farm.user_id == current_user.id,
            Crop.health_status == "diseased",
        )
    )

    diseased_crops = diseased_result.scalar() or 0

    # -----------------------------------------
    # Total diseases in knowledge/database
    # -----------------------------------------
    diseases_result = await db.execute(
        select(func.count(Disease.id))
    )

    total_diseases = diseases_result.scalar() or 0

    # -----------------------------------------
    # Soil type distribution
    # -----------------------------------------
    soil_result = await db.execute(
        select(
            Farm.soil_type,
            func.count(Farm.id)
        )
        .where(Farm.user_id == current_user.id)
        .group_by(Farm.soil_type)
    )

    soil_distribution = {}

    for soil_type, count in soil_result.all():
        soil_distribution[str(soil_type)] = count

    # -----------------------------------------
    # Crop distribution
    # -----------------------------------------
    crop_distribution_result = await db.execute(
        select(
            Crop.name,
            func.count(Crop.id)
        )
        .join(Farm, Crop.farm_id == Farm.id)
        .where(Farm.user_id == current_user.id)
        .group_by(Crop.name)
        .order_by(func.count(Crop.id).desc())
    )

    crop_distribution = [
        {
            "crop": crop_name,
            "count": count,
        }
        for crop_name, count in crop_distribution_result.all()
    ]

    # -----------------------------------------
    # Final response
    # -----------------------------------------
    return {
        "success": True,
        "data": {
            "total_farms": total_farms,
            "total_crops": total_crops,
            "total_diseases": total_diseases,
            "healthy_crops": healthy_crops,
            "warning_crops": warning_crops,
            "diseased_crops": diseased_crops,
            "soil_distribution": soil_distribution,
            "crop_distribution": crop_distribution,
        },
    }

