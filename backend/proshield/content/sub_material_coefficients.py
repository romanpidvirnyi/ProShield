import json
import os

from proshield import crud, schemas
from proshield.content.base import INIT_DATA_DIR
from sqlalchemy.orm import Session

FILE_NAME = "sub_material_coefficients.json"


def upload_sub_material_coefficients(db: Session):
    template_file_path = os.path.join(INIT_DATA_DIR, FILE_NAME)

    if not os.path.exists(template_file_path):
        return

    with open(template_file_path, "r") as file:
        data = json.load(file)

        for item in data:
            db_sub_material = crud.get_sub_material_by_name(
                db=db, name=item["sub_material_name"]
            )

            db_sub_material_coefficient = crud.get_sub_material_coefficient_by_params(
                db=db,
                sub_material_id=db_sub_material.id,
                thickness=item["thickness"],
            )

            if db_sub_material_coefficient is not None:
                crud.update_sub_material_coefficient(
                    db=db,
                    coefficient_id=db_sub_material.id,
                    coefficient=item["coefficient"],
                )
            else:
                crud.create_sub_material_coefficient(
                    db=db,
                    sub_material_id=db_sub_material.id,
                    thickness=item["thickness"],
                    coefficient=item["coefficient"],
                )
