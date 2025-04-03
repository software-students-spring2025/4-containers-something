from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017/")
db = client["ml_database"]
collection = db["sensor_data"]

@app.route("/")
def greet():
    return "Hello, World!"

@app.route("/data")
def get_data():
    # Just show the last inserted document (for placeholder purposes)
    latest = collection.find_one(sort=[("_id", -1)])
    if latest:
        latest["_id"] = str(latest["_id"])  # Convert ObjectId to string for JSON
    return jsonify(latest or {"message": "No data found."})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")  # host="0.0.0.0" makes it accessible from other containers
