"""
Unit testing for the web app
"""

import pytest
from app import app


@pytest.fixture
def test_client():
    """Fixture to create a test client for the Flask app."""
    with app.test_client() as client:
        yield client


def test_homepage(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
