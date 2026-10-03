import asyncio
from sqlalchemy import select
from app.database.database import AsyncSessionLocal
from app.models.treatment import Treatment

async def main():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Treatment))
        treatments = result.scalars().all()

        print("Total Treatments:", len(treatments))

        for t in treatments:
            print(
                t.id,
                "| Disease:", t.disease_id,
                "| Type:", t.recommendation_type,
                "| Description:", t.description
            )

asyncio.run(main())
