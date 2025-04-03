#placeholder!!
from datetime import datetime
from pymongo import MongoClient

#connect to mongodb running on localhost (from docker)
client = MongoClient("mongodb://mongodb:27017/")
db = client["ml_database"]
collection = db["sensor_data"]

def collect_data():
    #placeholder for actual sensor input
    return {
        "sensor_type": "placeholder",
        "value": 0,
        "timestamp": datetime.utcnow()
    }

def analyze_data(data):
    #placeholder analysis such as classification or stats
    data["analysis"] = "none"
    return data

def save_to_database(document):
    result = collection.insert_one(document)
    print(f"Saved document with _id: {result.inserted_id}")

if __name__ == "__main__":
    raw_data = collect_data()
    processed_data = analyze_data(raw_data)
    save_to_database(processed_data)
