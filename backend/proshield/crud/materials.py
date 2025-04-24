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


def get_sub_materials(
    material_id: int,
    db: Session,
    name: Optional[str] = None,
    density: Optional[float] = None,
) -> list[models.SubMaterial]:
    """
    Returns a SubMaterials list.

    Args:
        material_id (int): The Material ID.
        db (Session): Database session.

    Returns:
        list[models.SubMaterial]: SubMaterials list.
    """
    query = (
        select(models.SubMaterial)
        .where(models.SubMaterial.material_id == material_id)
        .distinct()
    )
    if name:
        query = query.where(models.SubMaterial.name == name)
    if density:
        query = query.where(models.SubMaterial.density == density)
    return db.scalars(query).all()


def get_sub_material_by_params(
    material_id: int,
    db: Session,
    name: str,
    density: float,
) -> Optional[models.SubMaterial]:
    """
    Returns a SubMaterial by params.

    Args:
        material_id (int): The Material ID.
        db (Session): Database session.
        name (str): The SubMaterial name.
        density (float): The SubMaterial density.

    Returns:
        Optional[models.SubMaterial]: The SubMaterial.
    """
    return db.scalars(
        select(models.SubMaterial)
        .where(
            models.SubMaterial.material_id == material_id,
            models.SubMaterial.name == name,
            models.SubMaterial.density == density,
        )
        .limit(1)
    ).first()


def create_sub_material(
    db: Session,
    sub_material: schemas.SubMaterialCreate,
) -> models.SubMaterial:
    """
    Creates new SubMaterial.

    Args:
        db (Session): The database session.
        sub_material (schemas.SubMaterialCreate): The SubMaterial to create.

    Returns:
        models.SubMaterial: The created SubMaterial.
    """
    db_sub_material = models.SubMaterial(
        material_id=sub_material.material_id,
        name=sub_material.name,
        density=sub_material.density,
    )

    db.add(db_sub_material)
    db.commit()
    db.refresh(db_sub_material)
    return db_sub_material


def get_sub_material_by_name(
    db: Session,
    name: str,
) -> Optional[models.SubMaterial]:
    """
    Returns a sub-material by name.

    Args:
        db (Session): Database session.
        name (str): The material name.

    Returns:
        Optional[models.SubMaterial]: The SubMaterial.
    """
    return db.scalars(
        select(models.SubMaterial).filter(models.SubMaterial.name == name).limit(1)
    ).first()


def get_sub_material_coefficient_by_params(
    db: Session,
    sub_material_id: Optional[int] = None,
    thickness: Optional[int] = None,
) -> Optional[models.AttenuationCoefficient]:
    """
    Returns a sub-material coefficient by params.

    Args:
        db (Session): Database session.
        sub_material_id (int): The material ID.
        thickness (int): The material thickness.

    Returns:
        Optional[models.SubMaterialCoefficient]: The SubMaterialCoefficient.
    """
    statement = select(models.SubMaterialCoefficient)

    if sub_material_id:
        statement = statement.filter(
            models.SubMaterialCoefficient.sub_material_id == sub_material_id
        )
    if thickness:
        statement = statement.filter(
            models.SubMaterialCoefficient.thickness == thickness
        )

    return db.scalars(statement.limit(1)).first()


def update_sub_material_coefficient(
    db: Session,
    coefficient_id: int,
    coefficient: float,
) -> models.SubMaterialCoefficient:
    """
    Update SubMaterialCoefficient.

    Args:
        db (Session): Database session.
        coefficient_id (int): The SubMaterial Coefficient ID.
        coefficient (float): The SubMaterial Coefficient to update.

    Returns (models.SubMaterialCoefficient):
        The SubMaterial Coefficient.
    """

    db_sub_material = db.get(models.SubMaterialCoefficient, coefficient_id)

    if db_sub_material is None:
        return None

    db_sub_material.coefficient = coefficient

    db.commit()
    db.refresh(db_sub_material)
    return db_sub_material


def create_sub_material_coefficient(
    db: Session,
    sub_material_id: int,
    thickness: int,
    coefficient: float,
) -> models.AttenuationCoefficient:
    """
    Creates new Attenuation Coefficient

     Args:
        db (Session): The database session.
        sub_material_id (int): The SubMaterial ID.
        thickness (int): The SubMaterial thickness.
        coefficient (float): The SubMaterial coefficient.

    Returns:
        models.SubMaterialCoefficient: The created SubMaterial Coefficient.
    """
    db_sub_material = models.SubMaterialCoefficient(
        sub_material_id=sub_material_id,
        thickness=thickness,
        coefficient=coefficient,
    )

    db.add(db_sub_material)
    db.commit()
    db.refresh(db_sub_material)
    return db_sub_material
