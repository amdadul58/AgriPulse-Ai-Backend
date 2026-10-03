import asyncio
from sqlalchemy import select
from app.database.database import AsyncSessionLocal
from app.models.disease import Disease

async def main():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Disease))
        diseases = result.scalars().all()

        print("Total Diseases:", len(diseases))

        for d in diseases:
            print(d.id, "|", d.name)

asyncio.run(main())
