"""Predicting a single ASL image to check if model was trained correctly."""

# pylint: disable=no-member, no-name-in-module, import-error

import cv2
import numpy as np
from tensorflow.keras.models import load_model

# === Config ===
MODEL_PATH = "sign_model.h5"
IMAGE_PATH = "dataset/asl_alphabet_train/A/A_100.jpg"
LABELS_PATH = "labels.txt"
IMG_SIZE = 100

# === Load model ===
model = load_model(MODEL_PATH)

# === Load labels ===
with open(LABELS_PATH, "r", encoding="utf-8") as f:
    LABELS = [line.strip() for line in f.readlines()]

# === Load and preprocess image ===
img = cv2.imread(IMAGE_PATH)  # pylint: disable=no-member
img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))  # pylint: disable=no-member
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # pylint: disable=no-member
img = img / 255.0
img = np.expand_dims(img, axis=0)  # Shape: (1, 100, 100, 3)

# === Predict ===
prediction = model.predict(img)
top_index = np.argmax(prediction)
confidence = float(prediction[0][top_index])
predicted_label = LABELS[top_index]

# === Output ===
print("Raw prediction:", prediction[0])
print("Predicted index:", top_index)
print(f"Predicted label: {predicted_label}, Confidence: {confidence:.2f}")
