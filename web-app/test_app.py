"""
Unit testing for the web app code
"""

# pylint: disable=redefined-outer-name

from unittest.mock import patch
import pytest
from app import app


@pytest.fixture
def client_fixture():
    """
    Create a test client for the Flask application.
    """
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
        "timestamp": "2025-04-03 13:45:00",
        "sign": "A",
        "confidence": 0.8,
    }
    mock_find_one.return_value = mock_data
    response = client_fixture.get("/data")
    assert response.status_code == 200
    assert b'"_id":"61d6c1d7f1b1c314ce875f23"' in response.data
    assert b'"timestamp":"2025-04-03 13:45:00"' in response.data
    assert b'"sign":"A"' in response.data
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
