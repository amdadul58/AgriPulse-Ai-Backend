from app.services.vector.chroma_service import ChromaVectorService
from app.services.vector.embedding_service import EmbeddingService

class Retriever:
    @staticmethod
    async def retrieve(query: str, top_k: int = 3):
        try:
            chroma = ChromaVectorService()
            if chroma.collection.count() == 0:
                return []
            query_emb = await EmbeddingService.get_embedding(query)
            results = chroma.collection.query(query_embeddings=[query_emb], n_results=top_k)
            if results and results['documents'] and results['documents'][0]:
                # None চেক করুন
                docs = [doc for doc in results['documents'][0] if doc is not None]
                return docs
            return []
        except Exception as e:
            print(f'Retriever Error: {e}')
            return []
