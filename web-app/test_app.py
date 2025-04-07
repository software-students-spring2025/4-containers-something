"""
Unit testing for the web app code
"""

import pytest
from app import app


@pytest.fixture
def client_fixture():
    """
    Create a test client for the Flask application.
    """
    with app.test_client() as client:
        yield client


def test_home_route(client_fixture):  # pylint: disable=redefined-outer-name
    """
    Test the home route to ensure it returns a status code of 200.
    """
    response = client_fixture.get("/")
    assert response.status_code == 200
