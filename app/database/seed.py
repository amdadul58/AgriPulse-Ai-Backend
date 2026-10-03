from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.disease import Disease
from app.services.vector.embedding_service import EmbeddingService
from app.services.vector.chroma_service import ChromaVectorService

import asyncio
from app.database.database import AsyncSessionLocal


async def seed_chroma_vectors(db: AsyncSession):

    chroma = ChromaVectorService()

    result = await db.execute(
        select(Disease)
    )

    diseases = result.scalars().all()

    print(f"Found Diseases: {len(diseases)}")


    for disease in diseases:

        print(f"Processing: {disease.name}")


        for crop in disease.affected_crops:

            text = f"""
            Crop: {crop}
            Disease: {disease.name}
            Symptoms: {disease.symptoms}
            """


            embedding = await EmbeddingService.get_embedding(
                text
            )


            chroma.add_disease(
                disease_id=str(disease.id),
                crop_name=crop,
                symptoms=disease.symptoms,
                embedding=embedding
            )


            print(
                f"Added to Chroma: {disease.name} - {crop}"
            )


    print(
        "Chroma vector seed completed successfully!"
    )



# FastAPI main.py startup এর জন্য
# main.py থেকে session পাঠানো হবে
async def seed_initial_diseases(db: AsyncSession):

    await seed_chroma_vectors(db)



# Manual command:
# python -m app.database.seed
async def run_seed():

    async with AsyncSessionLocal() as db:

        await seed_chroma_vectors(db)



if __name__ == "__main__":

    asyncio.run(run_seed())