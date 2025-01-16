import requests
from app.services.base import BASE_URL

STORAGE_CLASSES_URL = f"{BASE_URL}/attenuation-coefficients"


def get_attenuation_coefficients():
    response = requests.get(STORAGE_CLASSES_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return []
