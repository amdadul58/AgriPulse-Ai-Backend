import os
import uuid

from app.services.rag.chunk_service import ChunkService
from app.services.vector.embedding_service import EmbeddingService
from app.services.vector.chroma_service import ChromaVectorService


class IngestService:

    @staticmethod
    async def ingest_pdf(pdf_path: str):
        chroma = ChromaVectorService()

        text = ChunkService.extract_text_from_pdf(pdf_path)
        chunks = ChunkService.chunk_text(text)

        if not chunks:
            print(f"No text found in PDF: {pdf_path}")
            return

        for i, chunk in enumerate(chunks):
            embedding = await EmbeddingService.get_embedding(chunk)

            doc_id = f"pdf_{uuid.uuid4()}"

            chroma.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[
                    {
                        "source": os.path.basename(pdf_path),
                        "type": "pdf",
                        "chunk": i,
                    }
                ],
            )

        print(f"Ingested {len(chunks)} PDF chunks from {pdf_path}")

    @staticmethod
    async def ingest_text_file(file_path: str):
        chroma = ChromaVectorService()

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read().strip()
        except Exception as exc:
            print(f"Failed to read {file_path}: {exc}")
            return

        if not text:
            print(f"Empty document: {file_path}")
            return

        chunks = ChunkService.chunk_text(text)

        if not chunks:
            print(f"No chunks generated: {file_path}")
            return

        for i, chunk in enumerate(chunks):
            embedding = await EmbeddingService.get_embedding(chunk)

            doc_id = f"text_{uuid.uuid4()}"

            chroma.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[
                    {
                        "source": os.path.basename(file_path),
                        "type": "text",
                        "chunk": i,
                    }
                ],
            )

        print(f"Ingested {len(chunks)} chunks from {file_path}")

    @staticmethod
    async def ingest_knowledge_base(
        knowledge_base_path: str = "./knowledge_base"
    ):
        if not os.path.exists(knowledge_base_path):
            print(
                f"Knowledge base directory not found: "
                f"{knowledge_base_path}"
            )
            return

        total_files = 0

        for root, _, files in os.walk(knowledge_base_path):
            for filename in files:

                file_path = os.path.join(root, filename)
                extension = os.path.splitext(filename)[1].lower()

                try:
                    if extension == ".pdf":
                        await IngestService.ingest_pdf(file_path)
                        total_files += 1

                    elif extension in [".txt", ".md"]:
                        await IngestService.ingest_text_file(file_path)
                        total_files += 1

                except Exception as exc:
                    print(
                        f"Failed to ingest "
                        f"{file_path}: {exc}"
                    )

        chroma = ChromaVectorService()

        print("Knowledge base ingestion completed.")
        print(f"Files processed: {total_files}")
        print(
            f"Chroma collection count: "
            f"{chroma.collection.count()}"
        )