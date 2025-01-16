import requests
from app.services.base import BASE_URL

URL = f"{BASE_URL}/buildings-coefficients"


def get_buildings_coefficients():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        return []
