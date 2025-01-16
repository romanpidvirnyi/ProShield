from typing import Optional

from proshield import schemas
from proshield.db import models
from sqlalchemy import select, update
from sqlalchemy.orm import Session


def create_attenuation_coefficient(
    db: Session,
    attenuation_coefficient: schemas.AttenuationCoefficientCreate,
) -> models.AttenuationCoefficient:
    """
    Creates new Attenuation Coefficient

     Args:
        db (Session): The database session.
        attenuation_coefficient: The Attenuation Coefficient to create.

    Returns:
        models.AttenuationCoefficient: The created Attenuation Coefficient.
    """
    db_attenuation_coefficient = models.AttenuationCoefficient(
        material_id=attenuation_coefficient.material_id,
        material_thickness=attenuation_coefficient.material_thickness,
        material_density=attenuation_coefficient.material_density,
        neutron_dose_coefficient=attenuation_coefficient.neutron_dose_coefficient,
        gamma_dose_coefficient=attenuation_coefficient.gamma_dose_coefficient,
    )

    db.add(db_attenuation_coefficient)
    db.commit()
    db.refresh(db_attenuation_coefficient)
    return db_attenuation_coefficient


def get_attenuation_coefficient_by_id(
    db: Session,
    attenuation_coefficient_id: int,
) -> Optional[models.AttenuationCoefficient]:
    """
    Returns a attenuation coefficient by ID.

    Args:
        db (Session): Database session.
        attenuation_coefficient_id (int): The attenuation coefficient ID.

    Returns:
        Optional[models.AttenuationCoefficient]: The Attenuation Coefficient.
    """
    return db.scalars(
        select(models.AttenuationCoefficient)
        .filter(models.AttenuationCoefficient.id == attenuation_coefficient_id)
        .limit(1)
    ).first()


def get_attenuation_coefficient_by_params(
    db: Session,
    material_id: Optional[int] = None,
    material_thickness: Optional[int] = None,
) -> Optional[models.AttenuationCoefficient]:
    """
    Returns a attenuation coefficient by params.

    Args:
        db (Session): Database session.
        material_id (int): The material ID.
        material_thickness (int): The material thickness.

    Returns:
        Optional[models.AttenuationCoefficient]: The Attenuation Coefficient.
    """
    statement = select(models.AttenuationCoefficient)

    if material_id:
        statement = statement.filter(
            models.AttenuationCoefficient.material_id == material_id
        )
    if material_thickness:
        statement = statement.filter(
            models.AttenuationCoefficient.material_thickness == material_thickness
        )

    return db.scalars(statement.limit(1)).first()


def get_attenuation_coefficients(db: Session) -> list[models.AttenuationCoefficient]:
    """
    Returns a Attenuation Coefficients list.

    Args:
        db (Session): Database session.

    Returns:
        list[models.AttenuationCoefficient]: Attenuation Coefficients list.
    """
    return db.scalars(
        select(models.AttenuationCoefficient)
        .order_by(
            models.AttenuationCoefficient.material_id,
            models.AttenuationCoefficient.material_thickness,
        )
        .distinct()
    ).all()


def update_attenuation_coefficient(
    db: Session,
    attenuation_coefficient_id: int,
    attenuation_coefficient: schemas.AttenuationCoefficientUpdate,
) -> models.AttenuationCoefficient:
    """
    Update Attenuation Coefficient.

    Args:
        db (Session): Database session.
        attenuation_coefficient_id (int): The Attenuation Coefficient ID.
        attenuation_coefficient (schemas.AttenuationCoefficient): The Attenuation Coefficient to update.

    Returns (models.AttenuationCoefficient):
        The Attenuation Coefficient.
    """

    db_attenuation_coefficient = db.get(
        models.AttenuationCoefficient, attenuation_coefficient_id
    )

    if db_attenuation_coefficient is None:
        return None

    for key, value in attenuation_coefficient.model_dump(exclude_unset=True).items():
        setattr(db_attenuation_coefficient, key, value)

    db.commit()
    db.refresh(db_attenuation_coefficient)
    return db_attenuation_coefficient


def delete_attenuation_coefficient(db: Session, attenuation_coefficient_id: int):
    """
    Delete Attenuation Coefficient.

    Args:
        db (Session): Database session.
        attenuation_coefficient_id (int): The Attenuation Coefficient ID.

    """
    db_attenuation_coefficient = db.get(
        models.AttenuationCoefficient, attenuation_coefficient_id
    )

    if db_attenuation_coefficient is None:
        return None

    db.delete(db_attenuation_coefficient)
    db.commit()
