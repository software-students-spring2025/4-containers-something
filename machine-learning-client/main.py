import base64
from io import BytesIO
from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = tf.keras.models.load_model("sign_model.h5")

LABELS = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]

import logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=["GET"])
def home():
    """Default route for the root URL."""
    return "Welcome to the ASL Prediction API!"

@app.route("/predict", methods=["POST"])
def predict():
    """Accepts a base64-encoded image and returns predicted ASL letter."""
    data = request.get_json()
    logging.debug(f"Received data: {data.keys() if data else 'No data received'}")
    
    if "image" not in data:
        logging.error("No image provided in the request.")
        return jsonify({"error": "No image provided"}), 400

    try:
        # decode the base64 image
        image_data = base64.b64decode(data["image"].split(",")[1])
        img = Image.open(BytesIO(image_data)).resize((100, 100)).convert("RGB")
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

        # predict using the model
        prediction = model.predict(img_array)
        predicted_label = LABELS[np.argmax(prediction)]
        confidence = float(np.max(prediction))

        logging.debug(f"Prediction: {predicted_label}, Confidence: {confidence}")
        return jsonify({"prediction": predicted_label, "confidence": confidence})

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)