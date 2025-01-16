from fastapi import APIRouter, Depends, HTTPException, status
from proshield import crud, schemas
from proshield.core.database import get_db

router = APIRouter(prefix="")


@router.get(
    "",
    response_model=list[schemas.BuildingCoefficient],
    status_code=status.HTTP_200_OK,
)
def get_building_coefficients(
    db=Depends(get_db),
) -> list[schemas.BuildingCoefficient]:
    building_coefficients = crud.get_building_coefficients(db=db)
    return [
        schemas.BuildingCoefficient.model_validate(
            building_coefficient,
            from_attributes=True,
        )
        for building_coefficient in building_coefficients
    ]


@router.get(
    "/{building_coefficient_id}",
    response_model=schemas.BuildingCoefficient,
    status_code=status.HTTP_200_OK,
)
def get_building_coefficient(
    building_coefficient_id: int,
    db=Depends(get_db),
) -> schemas.BuildingCoefficient:
    building_coefficient = crud.get_building_coefficient_by_id(
        db=db,
        building_coefficient_id=building_coefficient_id,
    )

    if building_coefficient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BuildingCoefficient not found.",
        )

    return schemas.BuildingCoefficient.model_validate(
        building_coefficient,
        from_attributes=True,
    )


@router.post(
    "",
    response_model=schemas.BuildingCoefficient,
    status_code=status.HTTP_201_CREATED,
)
def create_building_coefficient(
    building_coefficient: schemas.BuildingCoefficientCreate,
    db=Depends(get_db),
) -> schemas.BuildingCoefficient:
    building_coefficient = crud.create_building_coefficient(
        db=db,
        building_coefficient=building_coefficient,
    )

    if building_coefficient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BuildingCoefficient not found.",
        )

    return schemas.BuildingCoefficient.model_validate(
        building_coefficient,
        from_attributes=True,
    )


@router.patch(
    "/{building_coefficient_id}",
    response_model=schemas.BuildingCoefficient,
    status_code=status.HTTP_200_OK,
)
def update_building_coefficient(
    building_coefficient_id: int,
    building_coefficient: schemas.BuildingCoefficientUpdate,
    db=Depends(get_db),
) -> schemas.BuildingCoefficient:
    building_coefficient = crud.update_building_coefficient(
        db=db,
        building_coefficient_id=building_coefficient_id,
        building_coefficient=building_coefficient,
    )

    if building_coefficient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BuildingCoefficient not found.",
        )

    return schemas.BuildingCoefficient.model_validate(
        building_coefficient,
        from_attributes=True,
    )


@router.delete(
    "/{building_coefficient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_building_coefficient(
    building_coefficient_id: int,
    db=Depends(get_db),
):
    crud.delete_building_coefficient(
        db=db, building_coefficient_id=building_coefficient_id
    )
