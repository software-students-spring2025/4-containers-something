"""Unit tests for main.py ASL prediction Flask app using pytest and Flask test client."""

import io
import pytest
from PIL import Image
from main import app


@pytest.fixture
def flask_client():
    """Creates a Flask test client for use in the test functions."""
    with app.test_client() as client:
        yield client


def test_predict_valid_image(flask_client):
    """Test /predict route with a valid image input."""
    img = Image.new("RGB", (100, 100), color="white")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    data = {"file": (img_bytes, "test.png")}
    response = flask_client.post("/predict", content_type="multipart/form-data", data=data)

    assert response.status_code == 200
    json_data = response.get_json()
    assert "prediction" in json_data
    assert "confidence" in json_data


def test_predict_no_file(flask_client):
    """Test /predict route with no file in the request."""
    response = flask_client.post("/predict", content_type="multipart/form-data", data={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "No file uploaded"}


def test_predict_empty_filename(flask_client):
    """Test /predict route with an empty filename."""
    data = {"file": (io.BytesIO(), "")}
    response = flask_client.post("/predict", content_type="multipart/form-data", data=data)
    assert response.status_code == 400
    assert response.get_json() == {"error": "Empty filename"}
