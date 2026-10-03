from sentence_transformers import SentenceTransformer
from app.core.config import settings


class EmbeddingService:

    model = None

    @classmethod
    def load_model(cls):
        if cls.model is None:
            cls.model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )
        return cls.model


    @classmethod
    async def get_embedding(cls, text: str) -> list:

        try:
            model = cls.load_model()

            embedding = model.encode(
                text,
                normalize_embeddings=True
            )

            return embedding.tolist()

        except Exception as e:
            print("Embedding Error:", e)
            raise Exception(
                f"Embedding generation failed: {e}"
            )