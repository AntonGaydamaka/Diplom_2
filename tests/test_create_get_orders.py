import allure
from utils.api_client import APIClient
from constants import APIEndpoints, TestData, Ingredients


@allure.epic("Заказы")
@allure.feature("Создание заказов")
class TestOrderEndpoint:
    """Тесты для заказов"""

    @allure.story("Создание заказа с авторизацией и валидными ингредиентами")
    @allure.title("Создание заказа (с авторизацией, валидные ингредиенты)")
    def test_create_order_with_auth_valid_ingredients(self, test_user):
        headers = {"Authorization": test_user["token"], "Content-Type": "application/json"}
        response = APIClient.post(APIEndpoints.ORDERS, {"ingredients": Ingredients.VALID}, headers=headers)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"

        with allure.step("Проверка успешности ответа"):
            response_json = response.json()
            assert response_json.get("success") is True, f"Ожидался success=True, но получен {response_json}"

        with allure.step("Проверка наличия данных о заказе"):
            assert "name" in response_json, "В ответе отсутствует поле 'name'"
            assert "order" in response_json and "number" in response_json[
                "order"], "В ответе отсутствует 'order' или 'number'"

    @allure.story("Создание заказа без авторизации и валидными ингредиентами")
    @allure.title("Создание заказа (без авторизации, валидные ингредиенты)")
    def test_create_order_without_auth_valid_ingredients(self):
        response = APIClient.post(APIEndpoints.ORDERS, {"ingredients": Ingredients.VALID}, headers=None)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"

        with allure.step("Проверка успешности ответа"):
            response_json = response.json()
            assert response_json.get("success") is True, f"Ожидался success=True, но получен {response_json}"

        with allure.step("Проверка наличия данных о заказе"):
            assert "name" in response_json, "В ответе отсутствует поле 'name'"
            assert "order" in response_json and "number" in response_json[
                "order"], "В ответе отсутствует 'order' или 'number'"

    @allure.story("Создание заказа с авторизацией и пустым списком ингредиентов")
    @allure.title("Создание заказа (с авторизацией, пустые ингредиенты)")
    def test_create_order_with_auth_empty_ingredients(self, test_user):
        headers = {"Authorization": test_user["token"], "Content-Type": "application/json"}
        response = APIClient.post(APIEndpoints.ORDERS, {"ingredients": Ingredients.EMPTY}, headers=headers)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            expected_message = {"success": False, "message": "Ingredient ids must be provided"}
            assert response.json() == expected_message, f"Ожидался ответ {expected_message}, но получен {response.json()}"

    @allure.story("Создание заказа с авторизацией и невалидными ингредиентами")
    @allure.title("Создание заказа (с авторизацией, невалидные ингредиенты)")
    def test_create_order_with_auth_invalid_ingredients(self, test_user):
        headers = {"Authorization": test_user["token"], "Content-Type": "application/json"}
        response = APIClient.post(APIEndpoints.ORDERS, {"ingredients": Ingredients.INVALID}, headers=headers)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 500, f"Ожидался статус 500, но получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            assert "Internal Server Error" in response.text, "Ожидалось сообщение 'Internal Server Error'"

    @allure.story("Создание заказа без авторизации и пустым списком ингредиентов")
    @allure.title("Создание заказа (без авторизации, пустые ингредиенты)")
    def test_create_order_without_auth_empty_ingredients(self):
        response = APIClient.post(APIEndpoints.ORDERS, {"ingredients": Ingredients.EMPTY}, headers=None)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            expected_message = {"success": False, "message": "Ingredient ids must be provided"}
            assert response.json() == expected_message, f"Ожидался ответ {expected_message}, но получен {response.json()}"

    @allure.story("Создание заказа без авторизации и невалидными ингредиентами")
    @allure.title("Создание заказа (без авторизации, невалидные ингредиенты)")
    def test_create_order_without_auth_invalid_ingredients(self):
        response = APIClient.post(APIEndpoints.ORDERS, {"ingredients": Ingredients.INVALID}, headers=None)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 500, f"Ожидался статус 500, но получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            assert "Internal Server Error" in response.text, "Ожидалось сообщение 'Internal Server Error'"

    @allure.story("Получение списка заказов пользователя")
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth(self, test_user):
        """
        Тест: Получение списка заказов авторизованного пользователя
        1. Создаем заказ
        2. Получаем заказы и проверяем данные
        """
        headers = {"Authorization": test_user["token"], "Content-Type": "application/json"}

        with allure.step("Создание нового заказа"):
            order_response = APIClient.post(APIEndpoints.ORDERS, TestData.ORDER_PAYLOAD, headers=headers)
            assert order_response.status_code == 200, f"Ошибка при создании заказа: {order_response.status_code}"
            order_json = order_response.json()

            assert order_json["success"] is True, "Ожидался success=True, но получен False"
            assert "order" in order_json, "Ответ не содержит данных о заказе"
            created_order = order_json["order"]

        with allure.step("Проверка соответствия ингредиентов"):
            created_ingredients = [ingredient["_id"] for ingredient in created_order["ingredients"]]
            assert created_ingredients == TestData.ORDER_PAYLOAD["ingredients"], "Список ингредиентов не совпадает"

        with allure.step("Проверка владельца заказа"):
            assert created_order["owner"]["name"] == test_user["name"], "Имя владельца заказа не совпадает"
            assert created_order["owner"]["email"] == test_user["email"], "Email владельца заказа не совпадает"

        with allure.step("Проверка статуса и имени заказа"):
            assert created_order["status"] == "done", "Статус заказа должен быть 'done'"
            assert created_order["name"], "Имя заказа отсутствует в ответе"

        with allure.step("Получение списка заказов пользователя"):
            get_orders_response = APIClient.get(APIEndpoints.ORDERS, headers=headers)
            assert get_orders_response.status_code == 200, f"Ошибка при получении заказов: {get_orders_response.status_code}"

            orders_json = get_orders_response.json()
            assert orders_json["success"] is True, "Ожидался success=True, но получен False"
            assert "orders" in orders_json, "Ответ не содержит списка заказов"

            user_orders = orders_json["orders"]
            assert any(order["name"] == created_order["name"] for order in
                       user_orders), "Созданный заказ отсутствует в списке заказов пользователя"

    @allure.story("Получение списка заказов без авторизации")
    @allure.title("Попытка получить заказы без авторизации")
    def test_get_orders_without_auth(self):
        """
        Тест: Попытка получения заказов без авторизации
        Ожидаемый результат:
        - Код ответа 401
        - Сообщение "You should be authorised"
        """

        with allure.step("Отправка GET-запроса без токена"):
            response = APIClient.get(APIEndpoints.ORDERS)

        with allure.step("Проверка ответа сервера"):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"

            expected_response = {"success": False, "message": "You should be authorised"}
            assert response.json() == expected_response, f"Ожидался ответ {expected_response}, но получен {response.json()}"
