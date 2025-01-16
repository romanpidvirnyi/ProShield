from typing import Optional

from proshield import schemas
from proshield.db import models
from sqlalchemy import select, update
from sqlalchemy.orm import Session


def create_wall_material(
    db: Session,
    material: schemas.WallMaterialCreate,
) -> models.WallMaterial:
    """
    Creates new material

     Args:
        db (Session): The database session.
        material (schemas.WallMaterialCreate): The material to create.

    Returns:
        models.WallMaterial: The created material.
    """
    db_material = models.WallMaterial(name=material.name)

    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def get_wall_material_by_id(
    db: Session,
    material_id: int,
) -> Optional[models.WallMaterial]:
    """
    Returns a material by ID.

    Args:
        db (Session): Database session.
        material_id (int): The material ID.

    Returns:
        Optional[models.WallMaterial]: The Material.
    """
    return db.scalars(
        select(models.WallMaterial)
        .filter(models.WallMaterial.id == material_id)
        .limit(1)
    ).first()


def get_wall_material_by_name(
    db: Session,
    name: str,
) -> Optional[models.WallMaterial]:
    """
    Returns a material by name.

    Args:
        db (Session): Database session.
        name (str): The material name.

    Returns:
        Optional[models.WallMaterial]: The WallMaterial.
    """
    return db.scalars(
        select(models.WallMaterial).filter(models.WallMaterial.name == name).limit(1)
    ).first()


def get_wall_materials(db: Session) -> list[models.WallMaterial]:
    """
    Returns a Materials list.

    Args:
        db (Session): Database session.

    Returns:
        list[models.WallMaterial]: Materials list.
    """
    return db.scalars(select(models.WallMaterial).distinct()).all()


def update_wall_material(
    db: Session,
    material_id: int,
    material: schemas.WallMaterialUpdate,
) -> models.WallMaterial:
    """
    Update Material.

    Args:
        db (Session): Database session.
        material_id (int): The Material ID.
        material (schemas.WallMaterialUpdate): The Material to update.

    Returns (models.WallMaterialUpdate):
        The material.
    """

    db_material = db.get(models.WallMaterial, material_id)

    if db_material is None:
        return None

    for key, value in material.model_dump(exclude_unset=True).items():
        setattr(db_material, key, value)

    db.commit()
    db.refresh(db_material)
    return db_material


def delete_wall_material(db: Session, material_id: int):
    """
    Delete Material.

    Args:
        db (Session): Database session.
        material_id (int): The Material ID.

    """
    db_material = db.get(models.WallMaterial, material_id)

    if db_material is None:
        return None

    db.delete(db_material)
    db.commit()
