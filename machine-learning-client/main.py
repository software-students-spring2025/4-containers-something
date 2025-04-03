from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np

# Load trained model
MODEL_PATH = "sign_model.h5" 
model = load_model(MODEL_PATH)
LABELS = sorted([
    "A", "B", "C", "D", "del", "E", "F", "G", "H", "I", "J", "K", "L",
    "M", "N", "nothing", "O", "P", "Q", "R", "S", "space", "T", "U",
    "V", "W", "X", "Y", "Z"
])

# Initialize Flask app
app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    """Accepts an image file and returns predicted digit."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        img = Image.open(file).resize((100, 100)).convert("RGB")
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        prediction = model.predict(img_array)
        predicted_label = LABELS[np.argmax(prediction)]
        confidence = float(np.max(prediction))

        return jsonify({"prediction": predicted_label, "confidence": confidence})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
