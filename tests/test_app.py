import pytest
from app import app

def test_main_route():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_form_elements():
    with app.test_client() as client:
        response = client.get('/')
        assert b'Intensity' in response.data
        assert b'g-recaptcha' in response.data