import json
import os

from app import crud, schemas
from app.content.base import TEMPLATES_DIR
from sqlalchemy.orm import Session

FILE_NAME = "materials.json"


def upload_materials(db: Session):
    template_file_path = os.path.join(TEMPLATES_DIR, FILE_NAME)

    if not os.path.exists(template_file_path):
        return

    with open(template_file_path, "r") as file:
        data = json.load(file)

        materials = [schemas.MaterialCreate(**item) for item in data]

        for material in materials:
            db_material = crud.get_material_by_name(db=db, name=material.name)

            if db_material is not None:
                crud.update_material(
                    db=db,
                    material_id=db_material.id,
                    material=material,
                )
            else:
                crud.create_material(db=db, material=material)
