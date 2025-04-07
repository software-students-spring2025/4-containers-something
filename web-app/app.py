"""Web Application for Displaying ML Client Data.

This Flask app connects to a MongoDB database and displays
the latest data collected and analyzed by the ML client.
"""

from flask import Flask, jsonify, render_template
from pymongo import MongoClient
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load env variables
load_dotenv()

username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

# Connect to MongoDB (inside a container named "mongodb")
client = MongoClient(os.getenv("URI"))
db = client["ml_database"]
collection = db["sensor_data"]


@app.route("/")
def home():
    """Render the home page (index.html)."""
    
    # Test DB connection
    # collection.insert_one({"name": "Test", "sentence": "HELLO WORLD WAHOO"})
    
    return render_template("index.html")


@app.route("/data")
def get_data():
    """Return the most recent sensor data as JSON."""
    latest = collection.find_one(sort=[("_id", -1)])
    if latest:
        latest["_id"] = str(latest["_id"])
    return jsonify(latest or {"message": "No data found."})


if __name__ == "__main__":
    # start Flask development server
    app.run(debug=True, host="0.0.0.0", port=5002)
