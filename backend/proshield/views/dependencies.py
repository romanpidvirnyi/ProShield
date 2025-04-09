import os
from pathlib import Path

from fastapi.templating import Jinja2Templates

# get path to templates directory
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_PATH = os.path.join(BASE_DIR, "templates")


def get_templates():
    return Jinja2Templates(directory=TEMPLATES_PATH)
