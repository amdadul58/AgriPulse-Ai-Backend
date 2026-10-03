import asyncio
from sqlalchemy import select

from app.database.database import AsyncSessionLocal
from app.models.disease import Disease


async def main():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Disease))
        diseases = result.scalars().all()

        print("=" * 50)
        print("Total Diseases:", len(diseases))
        print("=" * 50)

        for d in diseases:
            print("ID:", d.id)
            print("Name:", d.name)
            print("Affected Crops:", d.affected_crops)
            print("Symptoms:", d.symptoms)
            print("-" * 50)


asyncio.run(main())