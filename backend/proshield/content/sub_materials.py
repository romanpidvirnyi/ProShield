import json
import os

from proshield import crud, schemas
from proshield.content.base import INIT_DATA_DIR
from sqlalchemy.orm import Session

FILE_NAME = "sub_materials.json"


def upload_sub_materials(db: Session):
    template_file_path = os.path.join(INIT_DATA_DIR, FILE_NAME)

    if not os.path.exists(template_file_path):
        return

    with open(template_file_path, "r") as file:
        data = json.load(file)

        for item in data:
            db_material = crud.get_material_by_name(db=db, name=item["material_name"])

            db_sub_material = crud.get_sub_material_by_params(
                db=db,
                material_id=db_material.id,
                name=item["name"],
                density=item["density"],
            )

            if db_sub_material is None:
                crud.create_sub_material(
                    db=db,
                    sub_material=schemas.SubMaterialCreate(
                        material_id=db_material.id,
                        name=item["name"],
                        density=item["density"],
                    ),
                )
