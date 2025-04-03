"""
Machine Learning Client Script
This module simulates sensor data collection, processes it, and stores it in MongoDB.
"""

from datetime import datetime
from pymongo import MongoClient

# Connect to MongoDB (Docker container running on the same network)
client = MongoClient("mongodb://mongodb:27017/")
db = client["ml_database"]
collection = db["sensor_data"]


def collect_data():
    """Simulates data collection from a sensor."""
    return {
        "sensor_type": "placeholder",
        "value": 0,
        "timestamp": datetime.utcnow(),
    }


def analyze_data(data):
    """Processes and analyzes raw sensor data."""
    data["analysis"] = "none"
    return data


def save_to_database(document):
    """Inserts the document into the MongoDB collection."""
    result = collection.insert_one(document)
    print(f"Saved document with _id: {result.inserted_id}")


if __name__ == "__main__":
    raw_data = collect_data()
    processed_data = analyze_data(raw_data)
    save_to_database(processed_data)
