from app.services.vision.classifier import PlantDiseaseClassifier
from app.services.vision.image_service import ImageService


class DiseaseDetector:

    # Confidence threshold
    CONFIDENCE_THRESHOLD = 50.0

    @staticmethod
    async def detect(image_base64: str):

        try:

            if not image_base64:

                return {
                    "detected_disease": "No image provided",
                    "confidence": 0
                }

            # Decode base64 image
            image_bytes = ImageService.decode_base64(
                image_base64
            )

            # Run AI classifier
            result = await PlantDiseaseClassifier.classify_image(
                image_bytes
            )

            # ------------------------------------------------
            # MODEL ERROR
            # ------------------------------------------------

            if "error" in result:

                return {
                    "detected_disease": result["error"],
                    "confidence": 0
                }

            # ------------------------------------------------
            # BEST PREDICTION
            # ------------------------------------------------

            disease = result.get(
                "label",
                "Unknown"
            )

            plant = result.get(
                "plant",
                "Unknown"
            )

            confidence = float(
                result.get(
                    "confidence",
                    0
                )
            )

            full_label = result.get(
                "full_label",
                disease
            )

            top_predictions = result.get(
                "top_predictions",
                []
            )

            # ------------------------------------------------
            # LOW CONFIDENCE
            # ------------------------------------------------

            if confidence < DiseaseDetector.CONFIDENCE_THRESHOLD:

                return {
                    "detected_disease": "Uncertain",
                    "confidence": round(
                        confidence,
                        2
                    ),
                    "plant": plant,
                    "full_label": full_label,
                    "top_predictions": top_predictions,
                    "message": (
                        "The AI model is not confident "
                        "enough to identify this disease."
                    )
                }

            # ------------------------------------------------
            # HIGH CONFIDENCE
            # ------------------------------------------------

            return {
                "detected_disease": disease,
                "confidence": round(
                    confidence,
                    2
                ),
                "plant": plant,
                "full_label": full_label,
                "top_predictions": top_predictions
            }

        except Exception as e:

            return {
                "detected_disease": f"Error: {str(e)}",
                "confidence": 0
            }