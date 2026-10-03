from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.vector.chroma_service import ChromaVectorService
from app.services.vector.embedding_service import EmbeddingService


router = APIRouter(
    prefix="/vector",
    tags=["Vector"]
)


@router.post("/search")
async def vector_search(
    query: str = Query(..., min_length=1),
    top_k: int = Query(3, ge=1, le=10),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    ChromaDB Vector Search দিয়ে knowledge base থেকে
    সবচেয়ে relevant document খুঁজে বের করে।
    """

    try:
        chroma = ChromaVectorService()

        # Collection empty কিনা check
        collection_count = chroma.collection.count()

        if collection_count == 0:
            return {
                "query": query,
                "results": [],
                "message": "Vector database is empty."
            }

        # Query embedding তৈরি
        query_embedding = await EmbeddingService.get_embedding(query)

        # ChromaDB search
        results = chroma.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, collection_count),
            include=["documents", "metadatas", "distances"]
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        vector_results = []

        for doc, meta, distance in zip(
            documents,
            metadatas,
            distances
        ):
            vector_results.append(
                {
                    "document": doc,
                    "metadata": meta,
                    "distance": distance
                }
            )

        return {
            "query": query,
            "total_documents": collection_count,
            "results": vector_results
        }

    except Exception as e:
        return {
            "query": query,
            "results": [],
            "error": f"Vector Search Error: {str(e)}"
        }
