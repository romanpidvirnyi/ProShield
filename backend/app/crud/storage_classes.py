from typing import Optional

from app import schemas
from app.db import models
from sqlalchemy import select, update
from sqlalchemy.orm import Session


def create_storage_class(
    db: Session,
    storage_class: schemas.StorageClassCreate,
) -> models.StorageClass:
    """
    Creates new StorageClass

     Args:
        db (Session): The database session.
        storage_class (schemas.StorageClassCreate): The storage class to create.

    Returns:
        models.StorageClass: The created storage class.
    """
    db_storage_class = models.StorageClass(
        description=storage_class.description,
        protection_class=storage_class.protection_class,
        overpressure_air_blast_wave=storage_class.overpressure_air_blast_wave,
        radiation_protection_level=storage_class.radiation_protection_level,
    )

    db.add(db_storage_class)
    db.commit()
    db.refresh(db_storage_class)
    return db_storage_class


def get_storage_class_by_id(
    db: Session,
    storage_class_id: int,
) -> Optional[models.StorageClass]:
    """
    Returns a Storage Class by ID.

    Args:
        db (Session): Database session.
        storage_class_id (int): The Storage Class ID.

    Returns:
        Optional[models.StorageClass]: The Storage Class.
    """
    return db.scalars(
        select(models.StorageClass)
        .filter(models.StorageClass.id == storage_class_id)
        .limit(1)
    ).first()


def get_storage_class_by_protection_class(
    db: Session,
    protection_class: str,
) -> Optional[models.StorageClass]:
    """
    Returns a Storage Class by protection class.

    Args:
        db (Session): Database session.
        protection_class (str): The protection class.

    Returns:
        Optional[models.StorageClass]: The Storage Class.
    """
    return db.scalars(
        select(models.StorageClass)
        .filter(models.StorageClass.protection_class == protection_class)
        .limit(1)
    ).first()


def get_storage_classes(db: Session) -> list[models.StorageClass]:
    """
    Returns a Storage Classes list.

    Args:
        db (Session): Database session.

    Returns:
        list[models.StorageClass]: Storage Classes list.
    """
    return db.scalars(
        select(models.StorageClass)
        .order_by(models.StorageClass.protection_class)
        .distinct()
    ).all()


def update_storage_class(
    db: Session,
    storage_class_id: int,
    storage_class: schemas.StorageClassUpdate,
) -> models.StorageClass:
    """
    Update Storage Class.

    Args:
        db (Session): Database session.
        storage_class_id (int): The Storage Class ID.
        storage_class (schemas.StorageClassUpdate): The storage class to update.

    Returns (ProjectSettings):
        The project settings.
    """

    db_storage_class = db.get(models.StorageClass, storage_class_id)

    if db_storage_class is None:
        return None

    for key, value in storage_class.model_dump(exclude_unset=True).items():
        setattr(db_storage_class, key, value)

    db.commit()
    db.refresh(db_storage_class)
    return db_storage_class


def delete_storage_class(db: Session, storage_class_id: int):
    """
    Delete Storage Class.

    Args:
        db (Session): Database session.
        storage_class_id (int): The Storage Class ID.

    """
    db_storage_class = db.get(models.StorageClass, storage_class_id)

    if db_storage_class is None:
        return None

    db.delete(db_storage_class)
    db.commit()
