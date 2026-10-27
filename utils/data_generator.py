import random
import string


def random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_user():
    return {
        "email": f"{random_string()}@yandextestov.ruuuuu",
        "password": random_string(),
        "name": random_string(5)
    }


def generate_user1():
    """Генерирует случайные данные пользователя"""
    email = f"testuser{random.randint(1000, 9999)}@example.com"
    password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    name = "TestUser"
    return {"email": email, "password": password, "name": name}
