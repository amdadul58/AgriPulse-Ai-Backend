import os

import chromadb
from chromadb.config import Settings

from app.core.config import settings


class ChromaVectorService:

    _instance = None
    _collection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(
                ChromaVectorService, cls
            ).__new__(cls)

            cls._instance._initialize()

        return cls._instance

    def _initialize(self):
        os.makedirs(
            settings.CHROMA_PERSIST_DIR,
            exist_ok=True
        )

        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=Settings(
                anonymized_telemetry=False
            )
        )

        self._collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={
                "hnsw:space": "cosine"
            }
        )

    @property
    def collection(self):
        return self._collection

    # ---------------------------------------------------------
    # Add / Update Disease Vector
    # ---------------------------------------------------------

    def add_disease(
        self,
        disease_id: str,
        crop_name: str,
        symptoms: str,
        embedding: list
    ):
        """
        Disease information ChromaDB-তে store করে।
        একই disease-এর different crop-এর জন্য
        আলাদা vector ID তৈরি হবে।
        """

        vector_id = f"{disease_id}_{crop_name}"

        self._collection.upsert(
            ids=[vector_id],
            embeddings=[embedding],
            documents=[symptoms],
            metadatas=[
                {
                    "disease_id": disease_id,
                    "crop": crop_name,
                    "symptoms": symptoms
                }
            ]
        )

    # ---------------------------------------------------------
    # General Vector Search
    # ---------------------------------------------------------

    def search(
        self,
        query_embedding: list,
        top_k: int = 3
    ):
        """
        Knowledge Base-এর সাধারণ vector search।
        """

        collection_count = self._collection.count()

        if collection_count == 0:
            return {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]]
            }

        top_k = min(top_k, collection_count)

        return self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

    # ---------------------------------------------------------
    # Disease Vector Search
    # ---------------------------------------------------------

    def search_disease(
        self,
        query_embedding: list,
        top_k: int = 1
    ):
        """
        Disease vector search করে সবচেয়ে relevant
        disease ID return করে।
        """

        collection_count = self._collection.count()

        if collection_count == 0:
            return None

        top_k = min(top_k, collection_count)

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        if not results.get("ids"):
            return None

        if not results["ids"][0]:
            return None

        vector_id = results["ids"][0][0]

        # Example:
        # uuid_Tomato
        # uuid_Potato
        #
        # → uuid

        disease_id = vector_id.rsplit(
            "_",
            1
        )[0]

        return disease_id

