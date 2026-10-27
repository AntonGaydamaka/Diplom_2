import allure
from utils.api_client import APIClient
from constants import APIEndpoints, TestUserData, ErrorMessages


@allure.epic("Авторизация")
@allure.feature("Вход в систему")
class TestAuthLoginEndpoint:
    """Тесты авторизации"""

    @allure.story("Авторизация существующего пользователя")
    @allure.title("Успешный вход в систему")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_existing_user(self, test_user):
        """Тест авторизации существующего пользователя"""
        data = {"email": test_user["email"], "password": test_user["password"]}

        with allure.step("Отправка запроса на авторизацию"):
            response = APIClient.post(APIEndpoints.LOGIN, data)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"

        with allure.step("Проверка наличия accessToken в ответе"):
            assert "accessToken" in response.json(), "Ответ не содержит accessToken"

    @allure.story("Авторизация с неверными учетными данными")
    @allure.title("Попытка входа с неверными email и паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_invalid_credentials(self):
        """Тест авторизации с неверными учетными данными"""

        with allure.step("Отправка запроса на авторизацию с неверными данными"):
            response = APIClient.post(APIEndpoints.LOGIN, TestUserData.INVALID_CREDENTIALS)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            assert response.json() == ErrorMessages.INVALID_CREDENTIALS, \
                f"Ожидался ответ {ErrorMessages.INVALID_CREDENTIALS}, но получен {response.json()}"
