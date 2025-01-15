import json
import os

from proshield import crud, schemas
from proshield.content.base import TEMPLATES_DIR
from sqlalchemy.orm import Session

FILE_NAME = "attenuation_coefficients.json"


def upload_attenuation_coefficients(db: Session):
    template_file_path = os.path.join(TEMPLATES_DIR, FILE_NAME)

    if not os.path.exists(template_file_path):
        return

    with open(template_file_path, "r") as file:
        data = json.load(file)

        for item in data:
            db_material = crud.get_material_by_name(db=db, name=item["material_name"])

            db_attenuation_coefficient = crud.get_attenuation_coefficient_by_params(
                db=db,
                material_id=db_material.id,
                material_thickness=item["material_thickness"],
            )

            if db_attenuation_coefficient is not None:
                crud.update_attenuation_coefficient(
                    db=db,
                    attenuation_coefficient_id=db_attenuation_coefficient.id,
                    attenuation_coefficient=schemas.AttenuationCoefficientUpdate(
                        neutron_dose_coefficient=item["neutron_dose_coefficient"],
                        gamma_dose_coefficient=item["gamma_dose_coefficient"],
                    ),
                )
            else:
                crud.create_attenuation_coefficient(
                    db=db,
                    attenuation_coefficient=schemas.AttenuationCoefficientCreate(
                        material_id=db_material.id,
                        material_thickness=item["material_thickness"],
                        material_density=item["material_density"],
                        neutron_dose_coefficient=item["neutron_dose_coefficient"],
                        gamma_dose_coefficient=item["gamma_dose_coefficient"],
                    ),
                )
