import json
import os

from proshield import crud, schemas
from proshield.content.base import TEMPLATES_DIR
from sqlalchemy.orm import Session

FILE_NAME = "wall_materials.json"


def upload_wall_materials(db: Session):
    template_file_path = os.path.join(TEMPLATES_DIR, FILE_NAME)

    if not os.path.exists(template_file_path):
        return

    with open(template_file_path, "r") as file:
        data = json.load(file)

        materials = [schemas.WallMaterialCreate(**item) for item in data]

        for material in materials:
            db_material = crud.get_wall_material_by_name(db=db, name=material.name)

            if db_material is not None:
                crud.update_wall_material(
                    db=db,
                    material_id=db_material.id,
                    material=material,
                )
            else:
                crud.create_wall_material(db=db, material=material)
