"""
This module provides a Flask application for predicting ASL letters
from base64-encoded images using a TensorFlow model.
"""

import logging
import base64
from io import BytesIO
from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf
from flask_cors import CORS

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load the pre-trained TensorFlow model
model = tf.keras.models.load_model("sign_model.h5")  # pylint: disable=no-member

# Define the labels for ASL letters
LABELS = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]


@app.route("/", methods=["GET"])
def home():
    """Default route for the root URL."""
    return "Welcome to the ASL Prediction API!"


@app.route("/predict", methods=["POST"])
def predict():
    """Accepts a base64-encoded image and returns predicted ASL letter."""
    data = request.get_json()
    logging.debug("Received data: %s", data.keys() if data else "No data received")

    if not data or "image" not in data:
        logging.error("No image provided in the request.")
        return jsonify({"error": "No image provided"}), 400

    try:
        # Decode the base64 image
        image_data = base64.b64decode(data["image"].split(",")[1])
        img = Image.open(BytesIO(image_data)).resize((100, 100)).convert("RGB")
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

        # Predict using the model
        prediction = model.predict(img_array)
        predicted_label = LABELS[np.argmax(prediction)]
        confidence = float(np.max(prediction))

        logging.debug("Prediction: %s, Confidence: %f", predicted_label, confidence)
        return jsonify({"prediction": predicted_label, "confidence": confidence})

    except ValueError as e:
        logging.error("ValueError during prediction: %s", e)
        return jsonify({"error": str(e)}), 500
    except KeyError as e:
        logging.error("KeyError during prediction: %s", e)
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except IOError as e:
        logging.error("IOError during image processing: %s", e)
        return jsonify({"error": "Error processing the image"}), 500
    except Exception as e:  # pylint: disable=broad-exception-caught
        logging.error("Unexpected error during prediction: %s", e)
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
