"""Web Application for Displaying ML Client Data.

This Flask app connects to a MongoDB database and displays
the latest data collected and analyzed by the ML client.
"""

import os
from flask import (
    Flask,
    jsonify,
    render_template,
    redirect,
    request,
    flash,
    url_for,
    session,
)
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
)
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

app = Flask(__name__)
CORS(app)

# Load environment variables from the .env file
load_dotenv()

# Set the secret key for the session
app.secret_key = os.getenv("SECRET_KEY")  # Get secret key from the .env file

# Load MongoDB credentials
user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
pwd = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

# Connect to MongoDB (inside a container named "mongodb")
client = MongoClient(os.getenv("URI"))
db = client["ml_database"]
collection = db["sensor_data"]
users = db["users"]

# For login and logout with flash-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    """Class for flask-login users"""

    def __init__(self, user_id, username, is_active=True):
        self.id = str(user_id)
        self.username = username
        self._is_active = is_active

    def is_active_check(self):
        """Check for if user is logged in"""
        return self._is_active

    def is_authenticated_check(self):
        """Check for if user is authenticated"""
        return self.is_authenticated

    def get_id(self):
        """Returns current ID"""
        return self.id


@login_manager.user_loader
def load_user(user_id):
    """For flask-login use"""
    user_data = users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(
            user_id=user_data["_id"], username=user_data["username"], is_active=True
        )

    return None


@app.route("/")
def home():
    """Render the home page (index.html)."""
    user_id = session.get("user_id")

    if not user_id:
        return render_template("index.html", latest=[])

    try:
        user_id = ObjectId(user_id)
    except InvalidId:
        return render_template("index.html", latest=[])

    latest = collection.find({"user_id": user_id}, sort=[("_id", -1)])

    return render_template("index.html", latest=latest, user_id=user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Render the login page (login.html)."""
    # POST request
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_data = users.find_one({"username": username})

        if user_data:
            # check database for password
            if check_password_hash(user_data["password"], password):
                user_object = User(
                    user_id=user_data["_id"],
                    username=user_data["username"],
                    is_active=True,
                )

                session["user_id"] = str(user_data["_id"])

                login_user(user_object)
                flash("Logged in successfully!", "success")
                return redirect(url_for("home", username=username))

        flash("Invalid username or password.", "danger")
        return render_template("login.html")

    # GET request
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out and redirect to login page"""
    logout_user()
    session.pop("_flashes", None)
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Render the register page (register.html)"""
    # post request
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_doc = users.find_one({"username": username})
        if user_doc:
            flash("Username already exists. Please try again.", "error")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        users.insert_one({"username": username, "password": hashed_password})

        flash("Signed up successfully! Please login.", "success")
        return redirect(url_for("login"))

    # get request
    return render_template("register.html")


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
