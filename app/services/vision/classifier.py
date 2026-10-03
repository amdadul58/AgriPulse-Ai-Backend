import io
import json
import os

import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

from app.core.config import settings


class PlantDiseaseClassifier:

    _model = None
    _labels = None
    _model_loaded = False

    IMG_SIZE = (224, 224)

    @classmethod
    def load_model(cls):

        if cls._model is None:

            try:
                model_path = settings.VISION_MODEL_PATH

                print(f"🔍 Vision model path: {model_path}")
                print(f"🔍 Model exists: {os.path.exists(model_path)}")

                if not os.path.exists(model_path):

                    print(f"❌ Model not found: {model_path}")
                    cls._model_loaded = False
                    return None

                cls._model = load_model(
                    model_path,
                    compile=False
                )

                cls._model_loaded = True

                print("✅ Keras 3 Plant Disease Model loaded")
                print(f"📐 Model input shape: {cls._model.input_shape}")
                print(f"📊 Model output shape: {cls._model.output_shape}")

            except Exception as e:

                print("❌ Model loading error:", str(e))

                cls._model = None
                cls._model_loaded = False

        return cls._model

    @classmethod
    def load_labels(cls):

        if cls._labels is None:

            # Project root:
            # AgriPulse-Ai/ai_models/class_names.json
            project_root = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "..",
                    ".."
                )
            )

            label_path = os.path.join(
                project_root,
                "ai_models",
                "class_names.json"
            )

            print(f"🔍 Class names path: {label_path}")
            print(f"🔍 Labels exists: {os.path.exists(label_path)}")

            try:

                if not os.path.exists(label_path):

                    print(
                        f"❌ Class names file not found: {label_path}"
                    )

                    cls._labels = []
                    return cls._labels

                with open(
                    label_path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    cls._labels = json.load(f)

                print(
                    f"✅ Loaded {len(cls._labels)} class names"
                )

            except Exception as e:

                print(
                    "❌ Label loading error:",
                    str(e)
                )

                cls._labels = []

        return cls._labels

    @staticmethod
    def format_label(label: str):

        if "___" in label:

            plant_name, disease_name = label.split(
                "___",
                1
            )

            plant_name = (
                plant_name
                .replace("_", " ")
                .replace("(", "")
                .replace(")", "")
            )

            disease_name = (
                disease_name
                .replace("_", " ")
                .strip()
            )

            return plant_name, disease_name

        return "Unknown", label.replace("_", " ")

    @classmethod
    async def classify_image(
        cls,
        image_bytes: bytes
    ):

        try:

            model = cls.load_model()

            if not cls._model_loaded or model is None:

                return {
                    "error": "Vision model not loaded",
                    "confidence": 0
                }

            labels = cls.load_labels()

            if not labels:

                return {
                    "error": "Class names not loaded",
                    "confidence": 0
                }

            # Open image
            image = Image.open(
                io.BytesIO(image_bytes)
            ).convert("RGB")

            # Resize
            image = image.resize(
                cls.IMG_SIZE
            )

            # Convert to numpy
            img_array = np.array(
                image,
                dtype=np.float32
            )

            # IMPORTANT:
            # EfficientNet model already contains
            # its own Rescaling layer.
            #
            # Therefore DO NOT divide by 255 here.
            img_array = np.expand_dims(
                img_array,
                axis=0
            )

            # Prediction
            prediction = model.predict(
                img_array,
                verbose=0
            )

            probabilities = prediction[0]

            # Top-5 predictions
            top_indices = np.argsort(
                probabilities
            )[::-1][:5]

            top_predictions = []

            for index in top_indices:

                index = int(index)

                if index >= len(labels):
                    continue

                label = labels[index]

                confidence = float(
                    probabilities[index] * 100
                )

                plant_name, disease_name = (
                    cls.format_label(label)
                )

                top_predictions.append(
                    {
                        "plant": plant_name,
                        "disease": disease_name,
                        "confidence": round(
                            confidence,
                            2
                        ),
                        "full_label": label
                    }
                )

            if not top_predictions:

                return {
                    "error": "No valid prediction found",
                    "confidence": 0
                }

            best = top_predictions[0]

            return {
                "label": best["disease"],
                "plant": best["plant"],
                "confidence": best["confidence"],
                "full_label": best["full_label"],
                "top_predictions": top_predictions
            }

        except Exception as e:

            print(
                "❌ Vision Error:",
                str(e)
            )

            return {
                "error": f"Error: {str(e)}",
                "confidence": 0
            }