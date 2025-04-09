import json
import os

from proshield import crud, schemas
from proshield.content.base import INIT_DATA_DIR
from sqlalchemy.orm import Session

FILE_NAME = "building_coefficients.json"


def upload_building_coefficients(db: Session):
    template_file_path = os.path.join(INIT_DATA_DIR, FILE_NAME)

    if not os.path.exists(template_file_path):
        return

    with open(template_file_path, "r") as file:
        data = json.load(file)

        for item in data:
            db_building_type = crud.get_building_type_by_name(
                db=db, name=item["building_type_name"]
            )
            db_wall_material = crud.get_wall_material_by_name(
                db=db, name=item["wall_material_name"]
            )

            db_building_coefficient = crud.get_building_coefficient_by_params(
                db=db,
                building_type_id=db_building_type.id,
                wall_material_id=db_wall_material.id,
                wall_thickness=item["wall_thickness"],
                weight=item["weight"],
                area_relation_percent=item["area_relation_percent"],
            )

            if db_building_coefficient is not None:
                crud.update_building_coefficient(
                    db=db,
                    building_coefficient_id=db_building_coefficient.id,
                    building_coefficient=schemas.BuildingCoefficientUpdate(
                        coefficient=item["coefficient"],
                    ),
                )
            else:
                crud.create_building_coefficient(
                    db=db,
                    building_coefficient=schemas.BuildingCoefficientCreate(
                        building_type_id=db_building_type.id,
                        wall_material_id=db_wall_material.id,
                        wall_thickness=item["wall_thickness"],
                        weight=item["weight"],
                        area_relation_percent=item["area_relation_percent"],
                        coefficient=item["coefficient"],
                    ),
                )
