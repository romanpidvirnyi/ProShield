from typing import Optional

from proshield import schemas
from proshield.db import models
from sqlalchemy import select, update
from sqlalchemy.orm import Session


def create_material(
    db: Session,
    material: schemas.MaterialCreate,
) -> models.Material:
    """
    Creates new material

     Args:
        db (Session): The database session.
        material (schemas.MaterialCreate): The material to create.

    Returns:
        models.Material: The created material.
    """
    db_material = models.Material(name=material.name)

    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def get_material_by_id(
    db: Session,
    material_id: int,
) -> Optional[models.Material]:
    """
    Returns a material by ID.

    Args:
        db (Session): Database session.
        material_id (int): The material ID.

    Returns:
        Optional[models.Material]: The Material.
    """
    return db.scalars(
        select(models.Material).filter(models.Material.id == material_id).limit(1)
    ).first()


def get_material_by_name(
    db: Session,
    name: str,
) -> Optional[models.Material]:
    """
    Returns a material by name.

    Args:
        db (Session): Database session.
        name (str): The material name.

    Returns:
        Optional[models.Material]: The Material.
    """
    return db.scalars(
        select(models.Material).filter(models.Material.name == name).limit(1)
    ).first()


def get_materials(db: Session) -> list[models.Material]:
    """
    Returns a Materials list.

    Args:
        db (Session): Database session.

    Returns:
        list[models.Material]: Materials list.
    """
    return db.scalars(select(models.Material).distinct()).all()


def update_material(
    db: Session,
    material_id: int,
    material: schemas.MaterialUpdate,
) -> models.Material:
    """
    Update Material.

    Args:
        db (Session): Database session.
        material_id (int): The Material ID.
        material (schemas.MaterialUpdate): The Material to update.

    Returns (models.Material):
        The material.
    """

    db_material = db.get(models.Material, material_id)

    if db_material is None:
        return None

    for key, value in material.model_dump(exclude_unset=True).items():
        setattr(db_material, key, value)

    db.commit()
    db.refresh(db_material)
    return db_material


def delete_material(db: Session, material_id: int):
    """
    Delete Material.

    Args:
        db (Session): Database session.
        material_id (int): The Material ID.

    """
    db_material = db.get(models.Material, material_id)

    if db_material is None:
        return None

    db.delete(db_material)
    db.commit()
