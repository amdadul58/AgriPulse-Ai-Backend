from pathlib import Path
import tensorflow as tf
import json

BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_PATH = BASE_DIR / "ai_models" / "plant_disease_model.keras"
CLASS_PATH = BASE_DIR / "ai_models" / "class_names.json"

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_PATH, "r") as f:
    class_names = json.load(f)