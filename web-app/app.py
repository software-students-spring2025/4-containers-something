from flask import Flask, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017/")
db = client["ml_database"]
collection = db["sensor_data"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def get_data():
    latest = collection.find_one(sort=[("_id", -1)])
    if latest:
        latest["_id"] = str(latest["_id"])  # Convert ObjectId to string for JSON
    return jsonify(latest or {"message": "No data found."})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
