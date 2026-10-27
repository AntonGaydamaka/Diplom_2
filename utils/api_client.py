import requests
from constants import APIEndpoints


class APIClient:

    @staticmethod
    def post(endpoint, data, headers=None):
        return requests.post(f"{APIEndpoints.BASE_URL}{endpoint}", json=data, headers=headers)

    @staticmethod
    def get(endpoint, headers=None):
        return requests.get(f"{APIEndpoints.BASE_URL}{endpoint}", headers=headers)

    @staticmethod
    def patch(endpoint, data, headers=None):
        return requests.patch(f"{APIEndpoints.BASE_URL}{endpoint}", json=data, headers=headers)

    @staticmethod
    def delete(endpoint, headers=None):
        return requests.delete(f"{APIEndpoints.BASE_URL}{endpoint}", headers=headers)
