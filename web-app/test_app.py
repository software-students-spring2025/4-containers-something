"""
Unit testing for the web app code
"""

# pylint: disable=redefined-outer-name

from datetime import datetime
from unittest.mock import patch
import pytest
import mongomock
from app import app


@pytest.fixture(autouse=True)
def mock_database(monkeypatch):
    """
    Creates a mongo client to mocks a mongodb database
    """
    client = mongomock.MongoClient()
    database = client["testing_db"]
    mock_users = database["users"]
    monkeypatch.setattr("app.users", mock_users)
    yield mock_users


@pytest.fixture
def client_fixture():
    """
    Create a test client for the Flask application.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home(client_fixture):
    """
    Test the home route to ensure it returns a status code of 200 and
    renders the index.html with the expected content.
    """
    response = client_fixture.get("/")
    assert response.status_code == 200
    assert b"Sign Language Alphabet Detector" in response.data
    assert b"Live Detector" in response.data
    assert b"Your Signing History" in response.data


@patch(
    "app.collection.find_one"
)  # mocks find_one method for the collection sensor_data
def test_data_route_returned_data(mock_find_one, client_fixture):
    """
    Test the data route to ensure it returns the expected sensor data if there is stored data
    """
    mock_data = {
        "_id": "61d6c1d7f1b1c314ce875f23",
        "timestamp": datetime(2025, 4, 8, 19, 56, 6, 20300).isoformat(),
        "prediction": "A",
        "confidence": 0.8,
    }
    mock_find_one.return_value = mock_data
    response = client_fixture.get("/data")
    assert response.status_code == 200
    assert b'"_id":"61d6c1d7f1b1c314ce875f23"' in response.data
    assert b'"timestamp":"2025-04-08T19:56:06.020300"' in response.data
    assert b'"prediction":"A"' in response.data
    assert b'"confidence":0.8' in response.data


@patch("app.collection.find_one")
def test_data_route_no_data(mock_find_one, client_fixture):
    """
    Test the data route to ensure it returns an error message as JSON if no data is found
    """
    mock_find_one.return_value = None
    response = client_fixture.get("/data")
    assert response.status_code == 200
    assert b'{"message":"No data found."}' in response.data


def test_register_get_request(client_fixture):
    """
    Test the register route with get request
    """
    response = client_fixture.get("/register")
    assert response.status_code == 200
    assert b"Sign Up" in response.data


def test_register_new_user(client_fixture, mock_database):
    """
    Test the register route with a new user
    """
    response = client_fixture.post(
        "/register",
        data={"username": "test0", "password": "password0"},
        follow_redirects=True,
    )
    doc = mock_database.find_one({"username": "test0"})
    assert response.status_code == 200
    assert b"Login" in response.data
    assert doc is not None


def test_register_existing_user(client_fixture, mock_database):
    """
    Test the register route with an existing user
    """
    mock_database.insert_one({"username": "existing1", "password": "exists1"})
    response = client_fixture.post(
        "/register",
        data={"username": "existing1", "password": "randompw"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Username already exists. Please try again." in response.data


def test_login_get_request(client_fixture):
    """
    Test the login route with get request
    """
    response = client_fixture.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data
