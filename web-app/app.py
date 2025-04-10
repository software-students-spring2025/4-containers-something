"""Web Application for Displaying ML Client Data.

This Flask app connects to a MongoDB database and displays
the latest data collected and analyzed by the ML client.
"""

import os
from flask import Flask, jsonify, render_template, redirect, request, flash, url_for
from pymongo import MongoClient
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

# Set the secret key for the session
app.secret_key = os.getenv("SECRET_KEY")  # Get secret key from the .env file

# Load MongoDB credentials
username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

# Connect to MongoDB (inside a container named "mongodb")
client = MongoClient(os.getenv("URI"))
db = client["ml_database"]
collection = db["sensor_data"]
users = db["users"]


@app.route("/")
def home():
    """Render the home page (index.html)."""
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Render the login page (login.html)."""
    # POST request
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if users.find_one({"username": username, "password": password}):
            return redirect(url_for('home', username=username))
        else:
            flash("Invalid username or password.", "danger")
            return render_template("login.html")

    # GET request
    return render_template("login.html")


@app.route("/data")
def get_data():
    """Return the most recent sensor data as JSON."""
    latest = collection.find_one(sort=[("_id", -1)])
    if latest:
        latest["_id"] = str(latest["_id"])
    return jsonify(latest or {"message": "No data found."})


if __name__ == "__main__":
    # Start Flask development server
    app.run(debug=True, host="0.0.0.0", port=5002)
