import asyncio, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.core.config import settings
from app.models.disease import Disease
from app.services.vector.embedding_service import EmbeddingService
from app.services.vector.chroma_service import ChromaVectorService
async def ingest():
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as db:
        result = await db.execute(select(Disease))
        diseases = result.scalars().all()
        if not diseases: print('No diseases found'); return
        chroma = ChromaVectorService()
        for d in diseases:
            text = f'Crop: {', '.join(d.affected_crops or [])}. Symptoms: {d.symptoms}'
            emb = await EmbeddingService.get_embedding(text)
            chroma.add_disease(d.id, ', '.join(d.affected_crops or []), d.symptoms, emb)
            print(f'Ingested: {d.name}')
        print('Done')
if __name__ == '__main__': asyncio.run(ingest())
