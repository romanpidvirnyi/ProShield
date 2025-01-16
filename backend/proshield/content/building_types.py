import json
import os

from proshield import crud, schemas
from proshield.content.base import TEMPLATES_DIR
from sqlalchemy.orm import Session

FILE_NAME = "building_types.json"


def upload_building_types(db: Session):
    template_file_path = os.path.join(TEMPLATES_DIR, FILE_NAME)

    if not os.path.exists(template_file_path):
        return

    with open(template_file_path, "r") as file:
        data = json.load(file)

        building_types = [schemas.MaterialCreate(**item) for item in data]

        for building_type in building_types:
            db_building_type = crud.get_building_type_by_name(
                db=db, name=building_type.name
            )

            if db_building_type is not None:
                crud.update_building_type(
                    db=db,
                    building_type_id=db_building_type.id,
                    building_type=building_type,
                )
            else:
                crud.create_building_type(db=db, building_type=building_type)
