import json
import os

from proshield import crud, schemas
from proshield.content.base import TEMPLATES_DIR
from sqlalchemy.orm import Session

FILE_NAME = "location_condition_coefficients.json"


def upload_location_condition_coefficients(db: Session):
    template_file_path = os.path.join(TEMPLATES_DIR, FILE_NAME)

    if not os.path.exists(template_file_path):
        return

    with open(template_file_path, "r") as file:
        data = json.load(file)

        for item in data:
            db_building_type = crud.get_building_type_by_name(
                db=db, name=item["building_type_name"]
            )

            db_location_condition_coefficient = (
                crud.get_location_condition_coefficient_by_params(
                    db=db,
                    building_type_id=db_building_type.id,
                    building_height=item["building_height"],
                    building_density=item["building_density"],
                )
            )

            if db_location_condition_coefficient is not None:
                crud.update_location_condition_coefficient(
                    db=db,
                    location_condition_coefficient_id=db_location_condition_coefficient.id,
                    location_condition_coefficient=schemas.LocationConditionCoefficientUpdate(
                        coefficient=item["coefficient"],
                    ),
                )
            else:
                crud.create_location_condition_coefficient(
                    db=db,
                    location_condition_coefficient=schemas.LocationConditionCoefficientCreate(
                        building_type_id=db_building_type.id,
                        building_height=item["building_height"],
                        building_density=item["building_density"],
                        coefficient=item["coefficient"],
                    ),
                )
