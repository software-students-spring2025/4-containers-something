"""
Unit testing for the web app
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test the homepage."""
    response = client.get('/')
    assert response.status_code == 200
