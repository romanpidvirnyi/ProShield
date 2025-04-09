import json
import os

from proshield import crud, schemas
from proshield.content.base import INIT_DATA_DIR
from sqlalchemy.orm import Session

FILE_NAME = "storage_classes.json"


def upload_storage_classes(db: Session):
    template_file_path = os.path.join(INIT_DATA_DIR, FILE_NAME)

    if not os.path.exists(template_file_path):
        return

    with open(template_file_path, "r") as file:
        data = json.load(file)

        storage_classes = [schemas.StorageClassCreate(**item) for item in data]

        for storage_class in storage_classes:
            db_storage_class = crud.get_storage_class_by_protection_class(
                db=db, protection_class=storage_class.protection_class
            )

            if db_storage_class is not None:
                crud.update_storage_class(
                    db=db,
                    storage_class_id=db_storage_class.id,
                    storage_class=storage_class,
                )
            else:
                crud.create_storage_class(
                    db=db,
                    storage_class=storage_class,
                )
