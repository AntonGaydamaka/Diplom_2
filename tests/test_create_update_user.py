import allure
import pytest
from utils.api_client import APIClient
from constants import APIEndpoints, TestUserDataUpdate, ErrorMessages
from utils.data_generator import generate_user


@allure.epic("Пользователи")
@allure.feature("Работа с профилем")
class TestUserEndpoint:
    """Тесты для пользователя"""

    @allure.story("Получение данных пользователя")
    @allure.title("Проверка существования созданного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_unique_user(self, test_user):
        """Проверяет, что созданный пользователь существует"""
        with allure.step("Отправка запроса на получение данных пользователя"):
            response = APIClient.get(APIEndpoints.USER, headers={"Authorization": test_user["token"]})

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"

        with allure.step("Проверка, что email пользователя соответствует ожидаемому"):
            assert response.json()["user"]["email"] == test_user["email"], "Email пользователя не совпадает"

    @allure.story("Обновление email с авторизацией")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_email_with_auth(self, test_user):
        """Тест: Обновление email пользователя с авторизацией"""
        headers = {"Authorization": test_user["token"], "Content-Type": "application/json"}

        with allure.step("Отправляем запрос на обновление email"):
            response = APIClient.patch(APIEndpoints.USER, data={"email": TestUserDataUpdate.VALID_EMAIL},
                                       headers=headers)

        with allure.step("Проверяем, что email обновился корректно"):
            assert response.status_code == 200, f"Ошибка при обновлении email, статус {response.status_code}"
            assert response.json()["user"]["email"] == TestUserDataUpdate.VALID_EMAIL, "Email не обновился"

    @allure.story("Обновление имени с авторизацией")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_name_with_auth(self, test_user):
        """Тест: Обновление имени пользователя с авторизацией"""
        headers = {"Authorization": test_user["token"], "Content-Type": "application/json"}

        with allure.step("Отправляем запрос на обновление имени"):
            response = APIClient.patch(APIEndpoints.USER, data={"name": TestUserDataUpdate.VALID_NAME}, headers=headers)

        with allure.step("Проверяем, что имя обновилось корректно"):
            assert response.status_code == 200, f"Ошибка при обновлении имени, статус {response.status_code}"
            assert response.json()["user"]["name"] == TestUserDataUpdate.VALID_NAME, "Имя не обновилось"

    @allure.story("Обновление пароля с авторизацией")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_password_with_auth(self, test_user):
        """Тест: Обновление пароля пользователя с авторизацией"""
        headers = {"Authorization": test_user["token"], "Content-Type": "application/json"}

        with allure.step("Отправляем запрос на обновление пароля"):
            response = APIClient.patch(APIEndpoints.USER, data={"password": TestUserDataUpdate.VALID_PASSWORD},
                                       headers=headers)

        with allure.step("Проверяем, что статус ответа 200"):
            assert response.status_code == 200, f"Ошибка при обновлении пароля, статус {response.status_code}"

    @allure.story("Обновление email без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_email_without_auth(self):
        """Тест: Попытка обновления email без авторизации"""
        headers = {}  

        with allure.step("Отправляем запрос на обновление email без авторизации"):
            response = APIClient.patch(APIEndpoints.USER, data={"email": TestUserDataUpdate.UNAUTHORIZED_EMAIL},
                                       headers=headers)

        with allure.step("Проверяем, что возвращается ошибка 401"):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"
            assert response.json() == TestUserDataUpdate.UNAUTHORIZED_ERROR, "Сообщение об ошибке не совпадает"

    @allure.story("Обновление имени без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_name_without_auth(self):
        """Тест: Попытка обновления имени без авторизации"""
        headers = {}

        with allure.step("Отправляем запрос на обновление имени без авторизации"):
            response = APIClient.patch(APIEndpoints.USER, data={"name": TestUserDataUpdate.UNAUTHORIZED_NAME},
                                       headers=headers)

        with allure.step("Проверяем, что возвращается ошибка 401"):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"
            assert response.json() == TestUserDataUpdate.UNAUTHORIZED_ERROR, "Сообщение об ошибке не совпадает"

    @allure.story("Обновление пароля без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_password_without_auth(self):
        """Тест: Попытка обновления пароля без авторизации"""
        headers = {}

        with allure.step("Отправляем запрос на обновление пароля без авторизации"):
            response = APIClient.patch(APIEndpoints.USER, data={"password": TestUserDataUpdate.UNAUTHORIZED_PASSWORD},
                                       headers=headers)

        with allure.step("Проверяем, что возвращается ошибка 401"):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"
            assert response.json() == TestUserDataUpdate.UNAUTHORIZED_ERROR, "Сообщение об ошибке не совпадает"


@allure.epic("Пользователи")
@allure.feature("Регистрация")
class TestUserRegisterEndpoint:
    """Тесты регистрации пользователя"""

    @allure.story("Регистрация существующего пользователя")
    @allure.title("Попытка зарегистрировать уже существующего пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_existing_user(self, test_user):
        """Проверяет, что нельзя зарегистрировать уже существующего пользователя"""
        with allure.step("Отправка запроса на регистрацию уже существующего пользователя"):
            response = APIClient.post(APIEndpoints.REGISTER, test_user)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 403, f"Ожидался статус 403, но получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            assert response.json()["message"] == ErrorMessages.USER_EXISTS, "Сообщение об ошибке не совпадает"

    @pytest.mark.parametrize("field", TestUserDataUpdate.REQUIRED_FIELDS)
    @allure.story("Регистрация пользователя без обязательного поля")
    @allure.title("Регистрация без поля {field}")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_missing_field(self, field):
        """Проверяет, что регистрация невозможна без одного из обязательных полей"""
        user = generate_user()
        del user[field]

        with allure.step(f"Отправка запроса на регистрацию без поля {field}"):
            response = APIClient.post(APIEndpoints.REGISTER, user)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 403, f"Ожидался статус 403, но получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            assert response.json()["message"] == ErrorMessages.REQUIRED_FIELDS, "Сообщение об ошибке не совпадает"
