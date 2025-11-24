import pytest
import sys
import os
# Добавляем корень проекта в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

def test_main_route():
    """Проверяет что главная страница открывается"""
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_form_elements():
    """Проверяет что форма содержит нужные элементы"""
    with app.test_client() as client:
        response = client.get('/')
        assert b'Intensity' in response.data
