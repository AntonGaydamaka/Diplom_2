class APIEndpoints:
    """API эндпоинты"""
    BASE_URL = "https://qa-stellarburgers.education-services.ru/api"
    REGISTER = "/auth/register"
    USER = "/auth/user"
    ORDERS = "/orders"
    LOGIN = "/auth/login"


class Ingredients:
    """ID ингредиентов"""
    VALID = ["61c0c5a71d1f82001bdaaa7a", "61c0c5a71d1f82001bdaaa6f"]
    EMPTY = []
    INVALID = ["6c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f001bdaaa6f"]
    FULL = [
        "61c0c5a71d1f82001bdaaa7a",
        "61c0c5a71d1f82001bdaaa6f",
        "61c0c5a71d1f82001bdaaa77",
        "61c0c5a71d1f82001bdaaa79"
    ]


class ErrorMessages:
    """Ожидаемые сообщения об ошибках"""
    NO_INGREDIENTS = {"success": False, "message": "Ingredient ids must be provided"}
    SERVER_ERROR = "Internal Server Error"
    INVALID_CREDENTIALS = {"success": False, "message": "email or password are incorrect"}
    USER_EXISTS = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"


class TestData:
    """Тестовые данные"""
    ORDER_CASES = [
        (True, Ingredients.VALID, 200, None),
        (False, Ingredients.VALID, 200, None),
        (True, Ingredients.EMPTY, 400, ErrorMessages.NO_INGREDIENTS),
        (False, Ingredients.EMPTY, 400, ErrorMessages.NO_INGREDIENTS),
        (True, Ingredients.INVALID, 500, ErrorMessages.SERVER_ERROR),
        (False, Ingredients.INVALID, 500, ErrorMessages.SERVER_ERROR),
    ]

    ORDER_PAYLOAD = {"ingredients": Ingredients.FULL}


class TestUserData:
    """Тестовые данные для входа"""
    INVALID_CREDENTIALS = {"email": "wrong@example.com", "password": "wrongpass"}


class TestUserDataUpdate:
    """Тестовые данные пользователя"""

    # Тестовые данные для успешного обновления
    VALID_EMAIL = "updated_test@example.com"
    VALID_NAME = "UpdatedUser"
    VALID_PASSWORD = "NewPass123"

    # Тестовые данные для неавторизованного обновления
    UNAUTHORIZED_EMAIL = "unauthorized@example.com"
    UNAUTHORIZED_NAME = "UnauthorizedUser"
    UNAUTHORIZED_PASSWORD = "UnauthorizedPass"

    # Ожидаемое сообщение об ошибке при попытке обновления без авторизации
    UNAUTHORIZED_ERROR = {"success": False, "message": "You should be authorised"}

    REQUIRED_FIELDS = ["email", "password", "name"]
