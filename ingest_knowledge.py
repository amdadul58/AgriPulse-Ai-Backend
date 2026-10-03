import asyncio

from app.services.rag.ingest_service import IngestService


async def main():
    await IngestService.ingest_knowledge_base()


if __name__ == "__main__":
    asyncio.run(main())