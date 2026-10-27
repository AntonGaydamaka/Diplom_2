import pytest
import allure
from utils.api_client import APIClient
from constants import APIEndpoints
from utils.data_generator import generate_user


@pytest.fixture
def cleanup_user():
    """Фикстура для очистки пользователей после теста"""
    users_to_delete = []

    def register_for_cleanup(email, token):
        """Регистрирует пользователя для удаления после теста"""
        users_to_delete.append({"email": email, "token": token})

    yield register_for_cleanup

    # Удаляем всех зарегистрированных пользователей
    with allure.step("Очистка тестовых данных - удаление пользователей"):
        for user in users_to_delete:
            try:
                headers = {"Authorization": user["token"]}
                APIClient.delete(APIEndpoints.USER, headers=headers)
            except Exception as e:
                print(f"Ошибка при удалении пользователя {user['email']}: {e}")


@pytest.fixture
def test_user():
    """Фикстура создаёт условия для теста - подготавливает авторизованного пользователя"""
    user_data = generate_user()

    # Создание пользователя - подготовка условий для теста
    response = APIClient.post(APIEndpoints.REGISTER, user_data)
    assert response.status_code == 200, "Не удалось создать тестового пользователя"

    user_info = {
        "email": user_data["email"],
        "password": user_data["password"],
        "name": user_data["name"],
        "token": response.json()["accessToken"]
    }

    yield user_info

    # Удаляем пользователя после теста - очистка условий
    with allure.step("Очистка тестовых данных - удаление тестового пользователя"):
        try:
            headers = {"Authorization": user_info["token"]}
            APIClient.delete(APIEndpoints.USER, headers=headers)
        except Exception as e:
            print(f"Ошибка при удалении тестового пользователя: {e}")