import requests
from app.services.base import BASE_URL

BUILDING_TYPES_URL = f"{BASE_URL}/building-types"


def get_building_types():
    response = requests.get(BUILDING_TYPES_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return []
