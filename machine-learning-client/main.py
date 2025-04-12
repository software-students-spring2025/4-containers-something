"""
This module provides a Flask application for predicting ASL letters
from base64-encoded images using a TensorFlow model.
"""

import os
import base64
import logging
from datetime import datetime
from io import BytesIO

import numpy as np
from PIL import Image
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS

from bson import ObjectId
from bson.errors import InvalidId

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from dotenv import load_dotenv

# === setup ===
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

model = tf.keras.models.load_model("sign_model.h5")  # pylint: disable=no-member

load_dotenv()
client = MongoClient(os.getenv("URI"))
db = client["ml_database"]
collection = db["sensor_data"]

LABELS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

EXPORT_DIR = "exported_images"
os.makedirs(EXPORT_DIR, exist_ok=True)

# === helper functions ===


def decode_image(image_str):
    """Decode a base64 image string to raw bytes."""
    if "," in image_str:
        image_str = image_str.split(",")[1]
    return base64.b64decode(image_str)


def preprocess_image(image_data, crop_left, crop_right, resize_shape):
    """
    Crop and resize the image for model input.

    Args:
        image_data: Raw image bytes.
        crop_left: Pixels to crop from the left.
        crop_right: Pixels to crop from the right.
        resize_shape: Tuple (width, height) for resizing.

    Returns:
        Tuple of (resized PIL.Image, normalized numpy array).
    """
    img = Image.open(BytesIO(image_data)).convert("RGB")
    width, height = img.size
    cropped = img.crop((crop_left, 0, width - crop_right, height))
    resized = cropped.resize(resize_shape)
    return resized, np.expand_dims(np.array(resized) / 255.0, axis=0)


def save_image(image, prefix):
    """
    Save the processed image to disk with a timestamped filename.

    Args:
        image: PIL.Image to save.
        prefix: Prefix string for the filename.

    Returns:
        File path of the saved image.
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(EXPORT_DIR, f"{prefix}{timestamp}.jpg")
    image.save(filename)
    return filename


def make_prediction(img_array):
    """
    Run the model prediction on the preprocessed image.

    Args:
        img_array: Normalized numpy array of shape (1, H, W, 3).

    Returns:
        Tuple of (predicted label as string, confidence score as float).
    """
    prediction = model.predict(img_array)
    return LABELS[np.argmax(prediction)], float(np.max(prediction))


# === routes ===


@app.route("/", methods=["GET"])
def home():
    """Default route for basic health check."""
    return "Welcome to the ASL Prediction API!"


@app.route("/login", methods=["POST"])
def login():
    """Processes image and returns prediction for login image."""
    data = request.get_json()
    logging.debug("Received data: %s", data.keys() if data else "No data received")

    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    try:
        image_data = decode_image(data["image"])
        final_img, img_array = preprocess_image(
            image_data, crop_left=8, crop_right=80, resize_shape=(200, 200)
        )
        image_filename = save_image(final_img, prefix="login")
        predicted_label, confidence = make_prediction(img_array)

        logging.debug("Prediction: %s, Confidence: %f", predicted_label, confidence)

        return jsonify(
            {
                "prediction": predicted_label,
                "confidence": confidence,
                "image_path": image_filename,
            }
        )

    except ValueError as e:
        logging.error("ValueError during login: %s", e)
        return jsonify({"error": str(e)}), 500
    except KeyError as e:
        logging.error("KeyError during login: %s", e)
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except IOError as e:
        logging.error("IOError during image processing: %s", e)
        return jsonify({"error": "Error processing the image"}), 500
    except Exception as e:  # pylint: disable=broad-exception-caught
        logging.error("Unexpected error during login: %s", e)
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route("/predict", methods=["POST"])
def predict():
    """Processes image and returns prediction, optionally logging it to MongoDB."""
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    try:
        image_data = decode_image(data["image"])
        final_img, img_array = preprocess_image(
            image_data, crop_left=80, crop_right=80, resize_shape=(100, 100)
        )
        image_filename = save_image(final_img, prefix="predict")
        predicted_label, confidence = make_prediction(img_array)

        user_id = data.get("user_id")
        if user_id:
            try:
                mongo_id = ObjectId(user_id)
                entry = {
                    "timestamp": datetime.utcnow(),
                    "prediction": predicted_label,
                    "confidence": confidence,
                    "user_id": mongo_id,
                }
                collection.insert_one(entry)
                logging.info("Logged prediction for user %s", user_id)
            except (InvalidId, PyMongoError) as e:
                logging.warning("MongoDB error: %s", e)

        return jsonify(
            {
                "prediction": predicted_label,
                "confidence": confidence,
                "user_id": user_id,
                "image_path": image_filename,
            }
        )

    except (ValueError, KeyError, IOError, tf.errors.OpError) as e:
        logging.error("Unexpected error during prediction: %s", e)
        return jsonify({"error": str(e)}), 500


# === app entry ===

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
