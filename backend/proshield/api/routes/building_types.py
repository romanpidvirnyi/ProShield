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
    "/{building_type_id}/buildings-height",
    response_model=list[str],
    status_code=status.HTTP_200_OK,
)
def get_buildings_height(
    building_type_id: int,
    db=Depends(get_db),
) -> list[schemas.LocationConditionCoefficient]:
    buildings_height = crud.get_building_height_by_building_type(
        db=db, building_type_id=building_type_id
    )
    return buildings_height


@router.get(
    "/{building_type_id}/buildings-density",
    response_model=list[int],
    status_code=status.HTTP_200_OK,
)
def get_buildings_density(
    building_type_id: int,
    db=Depends(get_db),
) -> list[schemas.LocationConditionCoefficient]:
    buildings_density = crud.get_building_density_by_building_type(
        db=db, building_type_id=building_type_id
    )
    return buildings_density


@router.get(
    "/{building_type_id}/area-relation-percent",
    response_model=list[int],
    status_code=status.HTTP_200_OK,
)
def get_area_relation_percent(
    building_type_id: int,
    db=Depends(get_db),
) -> list[schemas.LocationConditionCoefficient]:
    area_relation_percents = crud.get_area_relation_percent(db=db)
    return area_relation_percents


@router.get(
    "/{building_type_id}/location-condition-coefficient",
    response_model=schemas.LocationConditionCoefficient,
    status_code=status.HTTP_200_OK,
)
def get_location_condition_coefficient(
    building_type_id: int,
    building_height: str,
    building_density: int,
    db=Depends(get_db),
) -> schemas.LocationConditionCoefficient:
    location_condition_coefficient = crud.get_location_condition_coefficient_by_params(
        db=db,
        building_type_id=building_type_id,
        building_height=building_height,
        building_density=building_density,
    )
    return location_condition_coefficient


@router.get(
    "/{building_type_id}/coefficient",
    response_model=schemas.BuildingCoefficient,
    status_code=status.HTTP_200_OK,
)
def get_building_coefficient(
    building_type_id: int,
    wall_material_id: int,
    wall_material_thickness: int,
    area_relation_percent: int,
    db=Depends(get_db),
) -> schemas.BuildingCoefficient:
    coefficient = crud.get_building_coefficient_by_params(
        db=db,
        building_type_id=building_type_id,
        wall_material_id=wall_material_id,
        wall_thickness=wall_material_thickness,
        area_relation_percent=area_relation_percent,
    )
    return coefficient


# @router.get(
#     "/{building_type_id}",
#     response_model=schemas.BuildingType,
#     status_code=status.HTTP_200_OK,
# )
# def get_building_type(
#     building_type_id: int,
#     db=Depends(get_db),
# ) -> schemas.BuildingType:
#     building_type = crud.get_building_type_by_id(
#         db=db,
#         building_type_id=building_type_id,
#     )

#     if building_type is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Building type not found.",
#         )

#     return schemas.BuildingType.model_validate(
#         building_type,
#         from_attributes=True,
#     )


# @router.post(
#     "",
#     response_model=schemas.BuildingType,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_building_type(
#     building_type: schemas.BuildingTypeCreate,
#     db=Depends(get_db),
# ) -> schemas.BuildingType:
#     building_type = crud.create_building_type(
#         db=db,
#         building_type=building_type,
#     )

#     if building_type is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Building type not found.",
#         )

#     return schemas.BuildingType.model_validate(
#         building_type,
#         from_attributes=True,
#     )


# @router.patch(
#     "/{building_type_id}",
#     response_model=schemas.BuildingType,
#     status_code=status.HTTP_200_OK,
# )
# def update_building_type(
#     building_type_id: int,
#     building_type: schemas.BuildingTypeUpdate,
#     db=Depends(get_db),
# ) -> schemas.BuildingTypeUpdate:
#     building_type = crud.update_building_type(
#         db=db, building_type_id=building_type_id, building_type=building_type
#     )

#     if building_type is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Building type not found.",
#         )

#     return schemas.BuildingType.model_validate(
#         building_type,
#         from_attributes=True,
#     )


# @router.delete(
#     "/{building_type_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# def delete_building_type(
#     building_type_id: int,
#     db=Depends(get_db),
# ):
#     crud.delete_building_type(db=db, building_type_id=building_type_id)
