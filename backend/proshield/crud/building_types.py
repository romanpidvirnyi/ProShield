from typing import Optional

from proshield import schemas
from proshield.db import models
from sqlalchemy import select, update
from sqlalchemy.orm import Session


def create_building_type(
    db: Session,
    building_type: schemas.BuildingTypeCreate,
) -> models.BuildingType:
    """
    Creates new building type

     Args:
        db (Session): The database session.
        building_type (schemas.BuildingTypeCreate): The building type to create.

    Returns:
        models.BuildingType: The created building type.
    """
    db_building_type = models.BuildingType(name=building_type.name)

    db.add(db_building_type)
    db.commit()
    db.refresh(db_building_type)
    return db_building_type


def get_building_type_by_id(
    db: Session,
    building_type_id: int,
) -> Optional[models.BuildingType]:
    """
    Returns a building type by ID.

    Args:
        db (Session): Database session.
        building_type_id (int): The building type ID.

    Returns:
        Optional[models.BuildingType]: The BuildingType.
    """
    return db.scalars(
        select(models.BuildingType)
        .filter(models.BuildingType.id == building_type_id)
        .limit(1)
    ).first()


def get_building_type_by_name(
    db: Session,
    name: str,
) -> Optional[models.BuildingType]:
    """
    Returns a building type by name.

    Args:
        db (Session): Database session.
        name (str): The building type name.

    Returns:
        Optional[models.BuildingType]: The BuildingType.
    """
    return db.scalars(
        select(models.BuildingType).filter(models.BuildingType.name == name).limit(1)
    ).first()


def get_building_types(db: Session) -> list[models.BuildingType]:
    """
    Returns a BuildingTypes list.

    Args:
        db (Session): Database session.

    Returns:
        list[models.BuildingType]: BuildingTypes list.
    """
    return db.scalars(select(models.BuildingType).distinct()).all()


def update_building_type(
    db: Session,
    building_type_id: int,
    building_type: schemas.BuildingTypeUpdate,
) -> models.BuildingType:
    """
    Update BuildingType.

    Args:
        db (Session): Database session.
        building_type_id (int): The BuildingType ID.
        building_type (schemas.BuildingTypeUpdate): The BuildingType to update.

    Returns (models.BuildingType):
        The building type.
    """

    db_building_type = db.get(models.BuildingType, building_type_id)

    if db_building_type is None:
        return None

    for key, value in building_type.model_dump(exclude_unset=True).items():
        setattr(db_building_type, key, value)

    db.commit()
    db.refresh(db_building_type)
    return db_building_type


def delete_building_type(db: Session, building_type_id: int):
    """
    Delete BuildingType.

    Args:
        db (Session): Database session.
        building_type_id (int): The BuildingType ID.

    """
    db_building_type = db.get(models.BuildingType, building_type_id)

    if db_building_type is None:
        return None

    db.delete(db_building_type)
    db.commit()
