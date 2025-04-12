import os
import logging
import base64
import numpy as np
from PIL import Image
from io import BytesIO
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import tensorflow as tf

# === Initialize Flask app ===
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# === Load environment variables ===
load_dotenv()

# === Load trained model (expects 100x100 input) ===
try:
    model = tf.keras.models.load_model("sign_model.h5")
    logging.info("✅ Model loaded successfully.")
except Exception as e:
    logging.error("❌ Failed to load model: %s", e)
    raise e

# === Setup MongoDB ===
try:
    print("Connecting to MongoDB at:", os.getenv("URI"))
    client = MongoClient(os.getenv("URI"))
    db = client["ml_database"]
    collection = db["sensor_data"]
    logging.info("✅ Connected to MongoDB.")
except Exception as e:
    logging.error("❌ MongoDB connection failed: %s", e)
    collection = None

# === Load label list ===
LABELS_FILE = "labels.txt"
if os.path.exists(LABELS_FILE):
    with open(LABELS_FILE, "r") as f:
        LABELS = [line.strip() for line in f.readlines()]
    logging.info("✅ Loaded labels from labels.txt.")
else:
    logging.warning("⚠️ labels.txt not found. Using fallback.")
    LABELS = [chr(c) for c in range(ord("A"), ord("C") + 1)]


# === Routes ===
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the ASL Prediction API!"


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data or "image" not in data:
            return jsonify({"error": "No image provided"}), 400

        image_base64 = data["image"]
        image_data = base64.b64decode(
            image_base64.split(",")[1] if "," in image_base64 else image_base64
        )

        # Load image
        img = Image.open(BytesIO(image_data)).convert("RGB")
        img.save("received_frame_original.jpg")  # Save full original image

        # Ensure it's 100x100
        img = img.resize((100, 100), Image.LANCZOS)
        img.save("received_frame_processed.jpg")

        # Prepare image array for model
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

        # Predict
        prediction = model.predict(img_array)

        # 🔍 DEBUG: print raw probabilities
        print("Raw prediction output:", prediction[0])

        top_index = np.argmax(prediction)
        print("Top index:", top_index)

        # 🔍 DEBUG: print full LABELS list
        print("Labels:", LABELS)

        # Check for index error
        if top_index >= len(LABELS):
            return jsonify({"error": "Prediction index out of range"}), 500

        predicted_label = LABELS[top_index]
        confidence = float(prediction[0][top_index])

        print(f"Predicted label: {predicted_label}, Confidence: {confidence:.2f}")

        # Log to DB
        if collection is not None:
            collection.insert_one(
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


# === Start app ===
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
