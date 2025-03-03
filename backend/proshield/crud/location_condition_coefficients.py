from typing import Optional

from proshield import schemas
from proshield.db import models
from sqlalchemy import select, update
from sqlalchemy.orm import Session


def create_location_condition_coefficient(
    db: Session,
    location_condition_coefficient: schemas.LocationConditionCoefficientCreate,
) -> models.LocationConditionCoefficient:
    """
    Creates new Location Condition Coefficient

     Args:
        db (Session): The database session.
        location_condition_coefficient: The Location Condition Coefficient to create.

    Returns:
        models.LocationConditionCoefficient: The Location Condition Coefficient.
    """
    db_location_condition_coefficient = models.LocationConditionCoefficient(
        building_type_id=location_condition_coefficient.building_type_id,
        building_height=location_condition_coefficient.building_height,
        building_density=location_condition_coefficient.building_density,
        coefficient=location_condition_coefficient.coefficient,
    )

    db.add(db_location_condition_coefficient)
    db.commit()
    db.refresh(db_location_condition_coefficient)
    return db_location_condition_coefficient


def get_location_condition_coefficient_by_id(
    db: Session,
    location_condition_coefficient_id: int,
) -> Optional[models.LocationConditionCoefficient]:
    """
    Returns a Location Condition Coefficient by ID.

    Args:
        db (Session): Database session.
        location_condition_coefficient_id (int): The Location Condition Coefficient ID.

    Returns:
        Optional[models.LocationConditionCoefficient]: The Location Condition Coefficient.
    """
    return db.scalars(
        select(models.LocationConditionCoefficient)
        .filter(
            models.LocationConditionCoefficient.id == location_condition_coefficient_id
        )
        .limit(1)
    ).first()


def get_location_condition_coefficient_by_params(
    db: Session,
    building_type_id: Optional[int] = None,
    building_height: Optional[str] = None,
    building_density: Optional[int] = None,
) -> Optional[models.LocationConditionCoefficient]:
    """
    Returns a LocationConditionCoefficient by params.

    Args:
        db (Session): Database session.
        building_type_id (int): The building type ID.
        building_height (str): The building height.
        building_density (int): The building density.

    Returns:
        Optional[models.LocationConditionCoefficient]: The LocationConditionCoefficient.
    """
    statement = select(models.LocationConditionCoefficient)

    if building_type_id:
        statement = statement.filter(
            models.LocationConditionCoefficient.building_type_id == building_type_id
        )
    if building_height:
        statement = statement.filter(
            models.LocationConditionCoefficient.building_height == building_height
        )
    if building_density:
        statement = statement.filter(
            models.LocationConditionCoefficient.building_density == building_density
        )

    return db.scalars(statement.limit(1)).first()


def get_location_condition_coefficients(
    db: Session,
) -> list[models.LocationConditionCoefficient]:
    """
    Returns a LocationConditionCoefficient list.

    Args:
        db (Session): Database session.

    Returns:
        list[models.LocationConditionCoefficient]: LocationConditionCoefficient list.
    """
    return db.scalars(
        select(models.LocationConditionCoefficient)
        .order_by(
            models.LocationConditionCoefficient.building_type_id,
            models.LocationConditionCoefficient.building_height,
            models.LocationConditionCoefficient.building_density.desc(),
        )
        .distinct()
    ).all()


def update_location_condition_coefficient(
    db: Session,
    location_condition_coefficient_id: int,
    location_condition_coefficient: schemas.LocationConditionCoefficientUpdate,
) -> models.LocationConditionCoefficient:
    """
    Update LocationConditionCoefficient.

    Args:
        db (Session): Database session.
        location_condition_coefficient_id (int): The LocationConditionCoefficient ID.
        location_condition_coefficient (schemas.LocationConditionCoefficientUpdate):
                                         The LocationConditionCoefficient to update.

    Returns (models.LocationConditionCoefficient):
        The LocationConditionCoefficient.
    """

    db_location_condition_coefficient = db.get(
        models.LocationConditionCoefficient, location_condition_coefficient_id
    )

    if db_location_condition_coefficient is None:
        return None

    for key, value in location_condition_coefficient.model_dump(
        exclude_unset=True
    ).items():
        setattr(db_location_condition_coefficient, key, value)

    db.commit()
    db.refresh(db_location_condition_coefficient)
    return db_location_condition_coefficient


def delete_location_condition_coefficient(
    db: Session, location_condition_coefficient_id: int
):
    """
    Delete LocationConditionCoefficient.

    Args:
        db (Session): Database session.
        location_condition_coefficient_id (int): The LocationConditionCoefficient ID.

    """
    location_condition_coefficient = db.get(
        models.LocationConditionCoefficient, location_condition_coefficient_id
    )

    if location_condition_coefficient is None:
        return None

    db.delete(location_condition_coefficient)
    db.commit()
