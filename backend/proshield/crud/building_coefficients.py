from typing import Optional

from proshield import schemas
from proshield.db import models
from sqlalchemy import select, update
from sqlalchemy.orm import Session


def create_building_coefficient(
    db: Session,
    building_coefficient: schemas.BuildingCoefficientCreate,
) -> models.BuildingCoefficient:
    """
    Creates new Building Coefficient

     Args:
        db (Session): The database session.
        building_coefficient: The Building Coefficient to create.

    Returns:
        models.BuildingCoefficient: The Building Coefficient.
    """
    db_building_coefficient = models.BuildingCoefficient(
        building_type_id=building_coefficient.building_type_id,
        wall_material_id=building_coefficient.wall_material_id,
        wall_thickness=building_coefficient.wall_thickness,
        weight=building_coefficient.weight,
        area_relation_percent=building_coefficient.area_relation_percent,
        coefficient=building_coefficient.coefficient,
    )

    db.add(db_building_coefficient)
    db.commit()
    db.refresh(db_building_coefficient)
    return db_building_coefficient


def get_area_relation_percent(db: Session) -> list[int]:
    return db.scalars(
        select(models.BuildingCoefficient.area_relation_percent)
        .order_by(models.BuildingCoefficient.area_relation_percent)
        .distinct()
    ).all()


def get_building_coefficient_by_id(
    db: Session,
    building_coefficient_id: int,
) -> Optional[models.BuildingCoefficient]:
    """
    Returns a Building Coefficient by ID.

    Args:
        db (Session): Database session.
        building_coefficient_id (int): The Building Coefficient ID.

    Returns:
        Optional[models.BuildingCoefficient]: The Building Coefficient.
    """
    return db.scalars(
        select(models.BuildingCoefficient)
        .filter(models.BuildingCoefficient.id == building_coefficient_id)
        .limit(1)
    ).first()


def get_building_coefficient_by_params(
    db: Session,
    wall_material_id: Optional[int] = None,
    building_type_id: Optional[int] = None,
    wall_thickness: Optional[int] = None,
    weight: Optional[int] = None,
    area_relation_percent: Optional[int] = None,
) -> Optional[models.BuildingCoefficient]:
    """
    Returns a LocationConditionCoefficient by params.

    Args:
        db (Session): Database session.
        wall_material_id (int): The wall material ID.
        building_type_id (int): The building type ID.
        wall_thickness (int): The wall thickness.
        weight (int): weight.
        area_relation_percent (int): The area relation percent.

    Returns:
        Optional[models.BuildingCoefficient]: The BuildingCoefficient.
    """
    statement = select(models.BuildingCoefficient)

    if wall_material_id:
        statement = statement.filter(
            models.BuildingCoefficient.wall_material_id == wall_material_id
        )
    if building_type_id:
        statement = statement.filter(
            models.BuildingCoefficient.building_type_id == building_type_id
        )
    if wall_thickness:
        statement = statement.filter(
            models.BuildingCoefficient.wall_thickness == wall_thickness
        )
    if weight:
        statement = statement.filter(models.BuildingCoefficient.weight == weight)
    if area_relation_percent:
        statement = statement.filter(
            models.BuildingCoefficient.area_relation_percent == area_relation_percent
        )

    return db.scalars(statement.limit(1)).first()


def get_building_coefficients(
    db: Session,
) -> list[models.BuildingCoefficient]:
    """
    Returns a BuildingCoefficient list.

    Args:
        db (Session): Database session.

    Returns:
        list[models.BuildingCoefficient]: BuildingCoefficient list.
    """
    return db.scalars(
        select(models.BuildingCoefficient)
        .order_by(
            models.BuildingCoefficient.wall_material_id,
            models.BuildingCoefficient.building_type_id,
            models.BuildingCoefficient.wall_thickness,
            models.BuildingCoefficient.weight,
        )
        .distinct()
    ).all()


def update_building_coefficient(
    db: Session,
    building_coefficient_id: int,
    building_coefficient: schemas.BuildingCoefficientUpdate,
) -> models.LocationConditionCoefficient:
    """
    Update BuildingCoefficient.

    Args:
        db (Session): Database session.
        building_coefficient_id (int): The BuildingCoefficient ID.
        building_coefficient (schemas.BuildingCoefficientUpdate):
                                    The BuildingCoefficient to update.

    Returns (models.BuildingCoefficient):
        The BuildingCoefficient.
    """

    db_building_coefficient = db.get(
        models.BuildingCoefficient, building_coefficient_id
    )

    if db_building_coefficient is None:
        return None

    for key, value in building_coefficient.model_dump(exclude_unset=True).items():
        setattr(db_building_coefficient, key, value)

    db.commit()
    db.refresh(db_building_coefficient)
    return db_building_coefficient


def delete_building_coefficient(db: Session, building_coefficient_id: int):
    """
    Delete BuildingCoefficient.

    Args:
        db (Session): Database session.
        building_coefficient_id (int): The BuildingCoefficient ID.

    """
    building_coefficient = db.get(models.BuildingCoefficient, building_coefficient_id)

    if building_coefficient is None:
        return None

    db.delete(building_coefficient)
    db.commit()
