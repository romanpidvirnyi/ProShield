import json
import os

from app import crud, schemas
from app.content.base import TEMPLATES_DIR
from app.content.materials import upload_materials
from app.content.storage_classes import upload_storage_classes
from sqlalchemy.orm import Session

FILE_NAME = "storage_classes.json"


def preload_templates(db: Session):
    # Створюємо в базі данних:
    # Класи сховищ, СПП із захисними властивостями сховищ
    upload_storage_classes(db=db)

    # Створюємо в базі данних: Матеріали
    upload_materials(db)
