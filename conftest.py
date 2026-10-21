import pytest
from utils.api_client import APIClient
from constants import APIEndpoints
from utils.data_generator import generate_user
import os
import shutil


@pytest.fixture
def test_user():
    """Создаёт тестового пользователя перед тестом и удаляет его после теста"""
    user = generate_user()

    response = APIClient.post(APIEndpoints.REGISTER, user)

    token = response.json().get("accessToken")

    
    user.update({
        "token": token,
        "email": response.json()["user"]["email"],
        "name": response.json()["user"]["name"],
        "password": user["password"]  
    })

    yield user  

    
    headers = {"Authorization": user["token"]}
    APIClient.delete(APIEndpoints.USER, headers=headers)


def pytest_sessionstart(session):
    """Очистка папки allure_results перед запуском тестов."""
    results_dir = "allure_results"
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    os.makedirs(results_dir)
