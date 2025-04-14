# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
"""Unit tests for main.py ASL prediction Flask app."""

import base64
from unittest.mock import patch, MagicMock
import pytest
from main import app


@pytest.fixture
def client():
    """Fixture for Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    """Test the health check route returns 200 OK."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the ASL Prediction API!" in response.data


@patch("main.model.predict")
@patch("main.Image.open")
@patch("main.SENSOR_DATA.insert_one")
def test_predict_success(mock_insert, mock_image_open, mock_model_predict, client):
    """Test successful image prediction."""
    mock_img = MagicMock()
    mock_img.resize.return_value = mock_img
    mock_img.convert.return_value = mock_img
    mock_image_open.return_value = mock_img
    mock_model_predict.return_value = [
        [0.0] * 4 + [0.9] + [0.0] * 21
    ]  # Label index 4 = "E"

    image_bytes = base64.b64encode(b"fake_image_data").decode("utf-8")
    response = client.post(
        "/predict", json={"image": f"data:image/png;base64,{image_bytes}"}
    )

    assert response.status_code == 200
    assert b"prediction" in response.data
    assert b"confidence" in response.data


def test_predict_missing_image(client):
    """Test /predict returns 400 on missing image."""
    response = client.post("/predict", json={})
    assert response.status_code == 400
    assert b"No image provided" in response.data


@patch("main.model.predict")
@patch("main.Image.open")
def test_predict_index_out_of_range(mock_image_open, mock_model_predict, client):
    """Test /predict returns 500 if prediction index is invalid."""
    mock_img = MagicMock()
    mock_img.resize.return_value = mock_img
    mock_img.convert.return_value = mock_img
    mock_image_open.return_value = mock_img

    mock_model_predict.return_value = [[0.0] * 26 + [1.0]]

    image_bytes = base64.b64encode(b"data").decode("utf-8")
    response = client.post("/predict", json={"image": image_bytes})
    assert response.status_code == 500


@patch("main.model.predict")
@patch("main.Image.open")
def test_predict_login_success(mock_image_open, mock_model_predict, client):
    """Test successful login prediction."""
    mock_img = MagicMock()
    mock_img.resize.return_value = mock_img
    mock_img.convert.return_value = mock_img
    mock_image_open.return_value = mock_img
    mock_model_predict.return_value = [[0.1] * 24 + [0.9] + [0.0]]  # Index 25 = "Z"

    image_bytes = base64.b64encode(b"another").decode("utf-8")
    response = client.post(
        "/predict_login", json={"image": f"data:image/png;base64,{image_bytes}"}
    )

    assert response.status_code == 200
    assert b"prediction" in response.data
    assert b"confidence" in response.data


def test_predict_login_no_image(client):
    """Test predict_login missing image input returns 400."""
    response = client.post("/predict_login", json={})
    assert response.status_code == 400
    assert b"No image provided" in response.data
