from fastapi import APIRouter, Depends, HTTPException, status
from proshield import crud, schemas
from proshield.core.database import get_db

router = APIRouter(prefix="")


@router.get(
    "",
    response_model=list[schemas.LocationConditionCoefficient],
    status_code=status.HTTP_200_OK,
)
def get_location_condition_coefficients(
    db=Depends(get_db),
) -> list[schemas.LocationConditionCoefficient]:
    location_condition_coefficient = crud.get_location_condition_coefficients(db=db)
    return [
        schemas.LocationConditionCoefficient.model_validate(
            location_condition_coefficient,
            from_attributes=True,
        )
        for location_condition_coefficient in location_condition_coefficient
    ]


@router.get(
    "/{location_condition_coefficient_id}",
    response_model=schemas.LocationConditionCoefficient,
    status_code=status.HTTP_200_OK,
)
def get_location_condition_coefficient(
    location_condition_coefficient_id: int,
    db=Depends(get_db),
) -> schemas.LocationConditionCoefficient:
    location_condition_coefficient = crud.get_location_condition_coefficient_by_id(
        db=db,
        location_condition_coefficient_id=location_condition_coefficient_id,
    )

    if location_condition_coefficient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LocationConditionCoefficient not found.",
        )

    return schemas.LocationConditionCoefficient.model_validate(
        location_condition_coefficient,
        from_attributes=True,
    )


@router.post(
    "",
    response_model=schemas.LocationConditionCoefficient,
    status_code=status.HTTP_201_CREATED,
)
def create_location_condition_coefficient(
    location_condition_coefficient: schemas.LocationConditionCoefficientCreate,
    db=Depends(get_db),
) -> schemas.LocationConditionCoefficient:
    location_condition_coefficient = crud.create_location_condition_coefficient(
        db=db,
        material=location_condition_coefficient,
    )

    if location_condition_coefficient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LocationConditionCoefficient not found.",
        )

    return schemas.LocationConditionCoefficient.model_validate(
        location_condition_coefficient,
        from_attributes=True,
    )


@router.patch(
    "/{location_condition_coefficient_id}",
    response_model=schemas.LocationConditionCoefficient,
    status_code=status.HTTP_200_OK,
)
def update_location_condition_coefficient(
    location_condition_coefficient_id: int,
    location_condition_coefficient: schemas.LocationConditionCoefficientUpdate,
    db=Depends(get_db),
) -> schemas.LocationConditionCoefficient:
    location_condition_coefficient = crud.update_location_condition_coefficient(
        db=db,
        location_condition_coefficient_id=location_condition_coefficient_id,
        location_condition_coefficient=location_condition_coefficient,
    )

    if location_condition_coefficient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LocationConditionCoefficient not found.",
        )

    return schemas.LocationConditionCoefficient.model_validate(
        location_condition_coefficient,
        from_attributes=True,
    )


@router.delete(
    "/{location_condition_coefficient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_location_condition_coefficient(
    location_condition_coefficient_id: int,
    db=Depends(get_db),
):
    crud.delete_location_condition_coefficient(
        db=db, location_condition_coefficient_id=location_condition_coefficient_id
    )
