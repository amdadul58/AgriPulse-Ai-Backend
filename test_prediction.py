import tensorflow as tf
import json
import numpy as np
from tensorflow.keras.preprocessing import image


# -----------------------------
# Paths
# -----------------------------
MODEL_PATH = "ai_models/plant_disease_model.keras"
CLASS_PATH = "ai_models/class_names.json"

# এখানে আপনার test image path দিন
IMAGE_PATH = "uploads/images/test_leaf.jpg"

# -----------------------------
# Load Model
# -----------------------------
print("Loading model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully!")


# -----------------------------
# Load Class Names
# -----------------------------
with open(CLASS_PATH, "r") as f:
    class_names = json.load(f)

print(f"Total Classes: {len(class_names)}")


# -----------------------------
# Image Preprocessing
# -----------------------------
# -----------------------------
# Image Preprocessing
# -----------------------------
# -----------------------------
# Image Preprocessing
# -----------------------------
IMG_SIZE = (224, 224)

print("Image Path:", IMAGE_PATH)

img = image.load_img(
    IMAGE_PATH,
    target_size=IMG_SIZE
)

img.show()

img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)

# Training-এর সাথে একই preprocessing
img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)

print("Min:", img_array.min())
print("Max:", img_array.max())
# -----------------------------
# Prediction
# -----------------------------
print("Predicting...")

prediction = model.predict(img_array)


predicted_index = np.argmax(prediction[0])

confidence = np.max(prediction[0])


disease_name = class_names[predicted_index]
top5 = np.argsort(prediction[0])[-5:][::-1]

print("\nTop 5 Predictions:")
for i in top5:
    print(f"{class_names[i]} : {prediction[0][i] * 100:.2f}%")

# -----------------------------
# Result
# -----------------------------
print("==============================")
print("Prediction Result")
print("==============================")

print("Disease :", disease_name)
print("Confidence :", round(confidence * 100, 2), "%")