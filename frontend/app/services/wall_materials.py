import requests
from app.services.base import BASE_URL

MATERIALS_URL = f"{BASE_URL}/wall-materials"


def get_wall_materials():
    response = requests.get(MATERIALS_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return []
