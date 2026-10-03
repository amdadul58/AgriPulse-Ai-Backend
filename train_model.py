# ============================================================
# AgriPulse-AI Plant Disease Training Script
# TensorFlow 2.21
# ============================================================

import os
import json
from pathlib import Path

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
)

# -----------------------------
# Configuration
# -----------------------------
IMG_SIZE = (224, 224)
BATCH_SIZE = 8
EPOCHS =1
SEED = 42

BASE_DIR = Path(__file__).resolve().parent

TRAIN_DIR = BASE_DIR / "dataset" / "PlantVillage" / "train"
VAL_DIR = BASE_DIR / "dataset" / "PlantVillage" / "val"

MODEL_DIR = BASE_DIR / "ai_models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "plant_disease_model.keras"
CLASS_PATH = MODEL_DIR / "class_names.json"

print("=" * 60)
print("AgriPulse AI Plant Disease Training")
print("=" * 60)

print(f"Train : {TRAIN_DIR}")
print(f"Valid : {VAL_DIR}")

# -----------------------------
# Load Dataset
# -----------------------------
train_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=SEED,
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    VAL_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False,
)

class_names = train_ds.class_names

print("\nClasses Found:")
for i, name in enumerate(class_names):
    print(f"{i+1:02d}. {name}")

print(f"\nTotal Classes: {len(class_names)}")

# Save class names
with open(CLASS_PATH, "w") as f:
    json.dump(class_names, f, indent=4)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = (
    train_ds
    .shuffle(1000)
    .prefetch(tf.data.AUTOTUNE)
)

val_ds = (
    val_ds
    .prefetch(tf.data.AUTOTUNE)
)

# -----------------------------
# Data Augmentation
# -----------------------------
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2),
    layers.RandomContrast(0.2),
])

# ============================================================
# Build EfficientNetB0 Model
# ============================================================

# Pre-trained EfficientNetB0 (ImageNet weights)
base_model = EfficientNetB0(
    include_top=False,
    weights="imagenet",
    input_shape=(224, 224, 3),
)

# প্রথম ধাপে base model freeze থাকবে
base_model.trainable = False

# Model Architecture
inputs = keras.Input(shape=(224, 224, 3))

# Data Augmentation
x = data_augmentation(inputs)

# Image preprocessing
x = tf.keras.applications.efficientnet.preprocess_input(x)

# Feature extraction
x = base_model(x, training=False)

# Classification Head
x = layers.GlobalAveragePooling2D()(x)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.30)(x)

x = layers.Dense(
    512,
    activation="relu",
    kernel_regularizer=keras.regularizers.l2(0.0005),
)(x)

x = layers.BatchNormalization()(x)
x = layers.Dropout(0.30)(x)

outputs = layers.Dense(
    len(class_names),
    activation="softmax",
    name="predictions",
)(x)

model = keras.Model(inputs, outputs)

# Compile
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

print("\nModel Summary:\n")
model.summary()

print("\nBase model frozen for initial training.")

# ============================================================
# Callbacks
# ============================================================

callbacks = [
    ModelCheckpoint(
        filepath=MODEL_PATH,
        monitor="val_accuracy",
        save_best_only=True,
        save_weights_only=False,
        verbose=1,
    ),

    EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
        verbose=1,
    ),

    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=2,
        min_lr=1e-6,
        verbose=1,
    ),
]

print("\nStarting Training...\n")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=callbacks,
)

print("\nTraining Finished Successfully!")

# ============================================================
# Evaluate Model
# ============================================================

loss, accuracy = model.evaluate(val_ds, verbose=1)

print("\n==============================")
print(f"Validation Loss     : {loss:.4f}")
print(f"Validation Accuracy : {accuracy*100:.2f}%")
print("==============================")

# নিশ্চিতভাবে সর্বশেষ মডেলও Save করা
model.save(MODEL_PATH)

print(f"\nModel Saved To:\n{MODEL_PATH}")
print(f"Class Names Saved To:\n{CLASS_PATH}")

# ============================================================
# Save Training History & Plots
# ============================================================

import matplotlib.pyplot as plt

HISTORY_PATH = MODEL_DIR / "training_history.json"

# Save history as JSON
with open(HISTORY_PATH, "w") as f:
    json.dump(history.history, f, indent=4)

print(f"\nTraining history saved to:\n{HISTORY_PATH}")

# -----------------------------
# Accuracy Plot
# -----------------------------
plt.figure(figsize=(8, 5))

plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")

plt.title("Model Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

accuracy_plot = MODEL_DIR / "accuracy.png"
plt.savefig(accuracy_plot, dpi=300)
plt.close()

# -----------------------------
# Loss Plot
# -----------------------------
plt.figure(figsize=(8, 5))

plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")

plt.title("Model Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

loss_plot = MODEL_DIR / "loss.png"
plt.savefig(loss_plot, dpi=300)
plt.close()

print(f"Accuracy graph saved : {accuracy_plot}")
print(f"Loss graph saved     : {loss_plot}")

# ============================================================
# Final Summary
# ============================================================

print("\n" + "=" * 60)
print("🎉 TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 60)
print(f"Classes           : {len(class_names)}")
print(f"Epochs            : {EPOCHS}")
print(f"Image Size        : {IMG_SIZE}")
print(f"Batch Size        : {BATCH_SIZE}")
print(f"Best Model        : {MODEL_PATH}")
print(f"Class Names       : {CLASS_PATH}")
print(f"Training History  : {HISTORY_PATH}")
print(f"Accuracy Plot     : {accuracy_plot}")
print(f"Loss Plot         : {loss_plot}")
print("=" * 60)