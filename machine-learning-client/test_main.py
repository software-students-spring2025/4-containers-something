import io
import pytest
from PIL import Image
from main import app  # only import the Flask app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_predict_valid_image(client):
    # Create a dummy white image in memory
    img = Image.new("RGB", (100, 100), color="white")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    # Send image to /predict
    response = client.post(
        "/predict",
        content_type="multipart/form-data",
        data={"file": (img_bytes, "test.png")},
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert "prediction" in json_data
    assert "confidence" in json_data
    assert isinstance(json_data["prediction"], str)
    assert isinstance(json_data["confidence"], float)


def test_predict_no_file(client):
    # No file in request
    response = client.post("/predict", content_type="multipart/form-data", data={})
    assert response.status_code == 400
    json_data = response.get_json()
    assert "error" in json_data


def test_predict_empty_file(client):
    # Simulate an empty filename
    response = client.post(
        "/predict",
        content_type="multipart/form-data",
        data={"file": (io.BytesIO(b""), "")},
    )
    assert response.status_code == 400
    json_data = response.get_json()
    assert "error" in json_data
