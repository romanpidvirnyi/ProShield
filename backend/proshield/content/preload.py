import json
import os

from proshield import crud, schemas
from proshield.content.attenuation_coefficients import upload_attenuation_coefficients
from proshield.content.base import INIT_DATA_DIR
from proshield.content.building_coefficients import upload_building_coefficients
from proshield.content.building_types import upload_building_types
from proshield.content.location_condition_coefficients import (
    upload_location_condition_coefficients,
)
from proshield.content.materials import upload_materials
from proshield.content.storage_classes import upload_storage_classes
from proshield.content.sub_material_coefficients import upload_sub_material_coefficients
from proshield.content.sub_materials import upload_sub_materials
from proshield.content.wall_materials import upload_wall_materials
from sqlalchemy.orm import Session

FILE_NAME = "storage_classes.json"


def preload_templates(db: Session):
    # Створюємо в базі данних:
    # Класи сховищ, СПП із захисними властивостями сховищ
    upload_storage_classes(db=db)

    # Створюємо в базі данних: Матеріали
    upload_materials(db)
    upload_sub_materials(db)
    upload_sub_material_coefficients(db)

    # Створюємо в базі данних:
    # Коефіцієнт послаблення дози гамма-випромінювання
    # та нейтронів проникаючої радіації товщею матеріалів
    upload_attenuation_coefficients(db)

    # Створюємо в базі данних: Характер забудови
    upload_building_types(db)

    # # Створюємо в базі данних: Коефіцієнт умов розташування
    upload_location_condition_coefficients(db)

    # Створюємо в базі данних: Матеріали стін будинків
    upload_wall_materials(db)
    # Створюємо в базі данних: Коефіцієнт будівель
    upload_building_coefficients(db)
