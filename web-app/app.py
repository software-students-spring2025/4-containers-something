"""Web Application for Displaying ML Client Data.

This Flask app connects to a MongoDB database and displays
the latest data collected and analyzed by the ML client.
"""

from flask import Flask, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB (inside a container named "mongodb")
client = MongoClient("mongodb://mongodb:27017/")
db = client["ml_database"]
collection = db["sensor_data"]

@app.route("/")
def home():
    """Render the home page (index.html)."""
    return render_template("index.html")

@app.route("/data")
def get_data():
    """Return the most recent sensor data as JSON."""
    latest = collection.find_one(sort=[("_id", -1)])
    if latest:
        latest["_id"] = str(latest["_id"])
    return jsonify(latest or {"message": "No data found."})

if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True, host="0.0.0.0", port=5001)
