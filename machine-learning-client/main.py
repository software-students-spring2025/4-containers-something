"""Main Flask application for ASL prediction."""

# pylint: disable=invalid-name
# pylint: disable=broad-exception-caught

import os
import base64
import logging
from datetime import datetime
from io import BytesIO

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from dotenv import load_dotenv
import numpy as np
from PIL import Image  # pylint: disable=import-error
# fmt: off
from tensorflow.keras.models import load_model  # pylint: disable=no-name-in-module, import-error
# fmt: on


# === Initialize Flask app ===
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# === Load environment variables ===
load_dotenv()

# === Load trained model (expects 100x100 input) ===
try:
    model = load_model("sign_model.h5")
    logging.info("✅ Model loaded successfully.")
except Exception as e:
    logging.error("❌ Failed to load model: %s", e)
    raise

# === Setup MongoDB ===
try:
    client = MongoClient(os.getenv("URI"))
    db = client["ml_database"]
    SENSOR_DATA = db["sensor_data"]
    logging.info("✅ Connected to MongoDB.")
except Exception as e:
    logging.error("❌ MongoDB connection failed: %s", e)
    SENSOR_DATA = None

# === Load label list ===
LABELS_FILE = "labels.txt"
if os.path.exists(LABELS_FILE):
    with open(LABELS_FILE, "r", encoding="utf-8") as f:
        LABELS = [line.strip() for line in f.readlines()]
    logging.info("✅ Loaded labels from labels.txt.")
else:
    logging.warning("⚠️ labels.txt not found. Using fallback.")
    LABELS = [chr(c) for c in range(ord("A"), ord("Z") + 1)]


@app.route("/", methods=["GET"])
def home():
    """Health check route."""
    return "Welcome to the ASL Prediction API!"


@app.route("/predict", methods=["POST"])
def predict():
    """Prediction endpoint using uploaded base64 image."""
    try:
        data = request.get_json()
        if not data or "image" not in data:
            return jsonify({"error": "No image provided"}), 400

        image_data = base64.b64decode(
            data["image"].split(",")[1] if "," in data["image"] else data["image"]
        )
        img = Image.open(BytesIO(image_data)).convert("RGB")
        img = img.resize((100, 100))  # pylint: disable=no-member
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

        prediction = model.predict(img_array)
        top_index = np.argmax(prediction)

        if top_index >= len(LABELS):
            return jsonify({"error": "Prediction index out of range"}), 500

        predicted_label = LABELS[top_index]
        confidence = float(prediction[0][top_index])

        if SENSOR_DATA:
            SENSOR_DATA.insert_one(
                {
                    "timestamp": datetime.utcnow(),
                    "prediction": predicted_label,
                    "confidence": confidence,
                }
            )

        return jsonify({"prediction": predicted_label, "confidence": confidence})

    except Exception as e:
        logging.exception("❗ Error during prediction")
        return jsonify({"error": str(e)}), 500


@app.route("/predict_login", methods=["POST", "OPTIONS"])
@cross_origin(origins=["http://127.0.0.1:5002"])
def predict_login():
    """Prediction endpoint for login page (image-only)."""
    try:
        data = request.get_json()
        if not data or "image" not in data:
            return jsonify({"error": "No image provided"}), 400

        image_data = base64.b64decode(
            data["image"].split(",")[1] if "," in data["image"] else data["image"]
        )
        img = Image.open(BytesIO(image_data)).convert("RGB")
        img = img.resize((100, 100))  # pylint: disable=no-member
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

        prediction = model.predict(img_array)
        top_index = np.argmax(prediction)

        if top_index >= len(LABELS):
            return jsonify({"error": "Prediction index out of range"}), 500

        predicted_label = LABELS[top_index]
        confidence = float(prediction[0][top_index])

        return jsonify({"prediction": predicted_label, "confidence": confidence})

    except Exception as e:
        logging.exception("❗ Error during predict_login")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
