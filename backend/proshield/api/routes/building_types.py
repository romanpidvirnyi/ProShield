from fastapi import APIRouter, Depends, HTTPException, status
from proshield import crud, schemas
from proshield.core.database import get_db

router = APIRouter(prefix="")


@router.get(
    "",
    response_model=list[schemas.BuildingType],
    status_code=status.HTTP_200_OK,
)
def get_building_types(db=Depends(get_db)) -> list[schemas.BuildingType]:
    building_types = crud.get_building_types(db=db)
    return [
        schemas.BuildingType.model_validate(
            building_type,
            from_attributes=True,
        )
        for building_type in building_types
    ]


@router.get(
    "/{building_type_id}",
    response_model=schemas.BuildingType,
    status_code=status.HTTP_200_OK,
)
def get_building_type(
    building_type_id: int,
    db=Depends(get_db),
) -> schemas.BuildingType:
    building_type = crud.get_building_type_by_id(
        db=db,
        building_type_id=building_type_id,
    )

    if building_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building type not found.",
        )

    return schemas.BuildingType.model_validate(
        building_type,
        from_attributes=True,
    )


@router.post(
    "",
    response_model=schemas.BuildingType,
    status_code=status.HTTP_201_CREATED,
)
def create_building_type(
    building_type: schemas.BuildingTypeCreate,
    db=Depends(get_db),
) -> schemas.BuildingType:
    building_type = crud.create_building_type(
        db=db,
        building_type=building_type,
    )

    if building_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building type not found.",
        )

    return schemas.BuildingType.model_validate(
        building_type,
        from_attributes=True,
    )


@router.patch(
    "/{building_type_id}",
    response_model=schemas.BuildingType,
    status_code=status.HTTP_200_OK,
)
def update_building_type(
    building_type_id: int,
    building_type: schemas.BuildingTypeUpdate,
    db=Depends(get_db),
) -> schemas.BuildingTypeUpdate:
    building_type = crud.update_building_type(
        db=db, building_type_id=building_type_id, building_type=building_type
    )

    if building_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building type not found.",
        )

    return schemas.BuildingType.model_validate(
        building_type,
        from_attributes=True,
    )


@router.delete(
    "/{building_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_building_type(
    building_type_id: int,
    db=Depends(get_db),
):
    crud.delete_building_type(db=db, building_type_id=building_type_id)
