from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.disease import Disease
from app.models.treatment import Treatment

from app.services.vector.embedding_service import EmbeddingService
from app.services.vector.chroma_service import ChromaVectorService


class CropAdvisorService:

    @staticmethod
    async def detect_disease_and_suggest(
        db: AsyncSession,
        crop_name: str,
        symptoms: str
    ):
        """
        Detect disease using Chroma vector search,
        then fetch the matching Disease and Treatments
        from PostgreSQL.

        IMPORTANT:
        We do NOT assign to disease.treatments here.
        That can trigger SQLAlchemy async lazy-loading
        and cause MissingGreenlet.
        """

        try:
            # ==================================================
            # 1. Create search text
            # ==================================================
            query_text = (
                f"Crop: {crop_name}. "
                f"Symptoms: {symptoms}"
            )

            print("=" * 60)
            print("Disease Detection")
            print("Crop:", crop_name)
            print("Symptoms:", symptoms)

            # ==================================================
            # 2. Generate embedding
            # ==================================================
            query_vector = await EmbeddingService.get_embedding(
                query_text
            )

            print(
                "Embedding dimension:",
                len(query_vector)
            )

            # ==================================================
            # 3. Search Chroma
            # ==================================================
            chroma = ChromaVectorService()

            disease_id = chroma.search_disease(
                query_embedding=query_vector,
                top_k=1
            )

            print(
                "Chroma Disease ID:",
                disease_id
            )

            if not disease_id:
                print(
                    "No matching disease found in Chroma."
                )
                return None

            # ==================================================
            # 4. Find Disease in PostgreSQL
            # ==================================================
            result = await db.execute(
                select(Disease).where(
                    Disease.id == str(disease_id)
                )
            )

            disease = result.scalar_one_or_none()

            if disease is None:
                print(
                    "Disease exists in Chroma but was "
                    "not found in PostgreSQL."
                )
                print(
                    "Chroma ID:",
                    disease_id
                )

                return None

            print(
                "Database Disease:",
                disease.name
            )

            print(
                "Database Disease ID:",
                disease.id
            )

            # ==================================================
            # 5. Get Treatments separately
            # ==================================================
            treatment_result = await db.execute(
                select(Treatment).where(
                    Treatment.disease_id == str(disease.id)
                )
            )

            treatments = treatment_result.scalars().all()

            print(
                "Treatments Found:",
                len(treatments)
            )

            for treatment in treatments:
                print(
                    "Treatment:",
                    treatment.id,
                    treatment.recommendation_type
                )

            # ==================================================
            # IMPORTANT
            # ==================================================
            #
            # DO NOT DO THIS:
            #
            # disease.treatments = treatments
            #
            # Because `treatments` is an SQLAlchemy relationship.
            # In AsyncSession, assigning it can cause SQLAlchemy
            # to lazy-load the existing relationship and produce:
            #
            # sqlalchemy.exc.MissingGreenlet
            #
            # Therefore return both objects separately.
            #
            # ==================================================

            return disease, treatments

        except Exception as e:

            import traceback

            print("=" * 60)
            print(
                "ERROR IN detect_disease_and_suggest"
            )
            print("=" * 60)

            traceback.print_exc()

            return None

    # ==========================================================
    # Get treatments for a disease
    # ==========================================================

    @staticmethod
    async def get_recommendations_for_disease(
        db: AsyncSession,
        disease_id: str
    ):
        """
        Return all treatments belonging to a disease.
        """

        try:

            result = await db.execute(
                select(Treatment).where(
                    Treatment.disease_id == str(disease_id)
                )
            )

            treatments = result.scalars().all()

            return treatments

        except Exception as e:

            import traceback

            print("=" * 60)
            print(
                "ERROR IN get_recommendations_for_disease"
            )
            print("=" * 60)

            traceback.print_exc()

            return []