from fastapi import APIRouter, Depends, HTTPException, status
from proshield import crud, schemas
from proshield.core.database import get_db

router = APIRouter(prefix="")


@router.get(
    "",
    response_model=list[schemas.AttenuationCoefficient],
    status_code=status.HTTP_200_OK,
)
def get_attenuation_coefficient(
    db=Depends(get_db),
) -> list[schemas.AttenuationCoefficient]:
    attenuation_coefficients = crud.get_attenuation_coefficients(db=db)
    return [
        schemas.AttenuationCoefficient.model_validate(
            attenuation_coefficient,
            from_attributes=True,
        )
        for attenuation_coefficient in attenuation_coefficients
    ]


# @router.get(
#     "/{attenuation_coefficient_id}",
#     response_model=schemas.AttenuationCoefficient,
#     status_code=status.HTTP_200_OK,
# )
# def get_attenuation_coefficient(
#     attenuation_coefficient_id: int,
#     db=Depends(get_db),
# ) -> schemas.AttenuationCoefficient:
#     attenuation_coefficient = crud.get_attenuation_coefficient_by_id(
#         db=db,
#         material_id=attenuation_coefficient_id,
#     )

#     if attenuation_coefficient is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Attenuation Coefficient not found.",
#         )

#     return schemas.AttenuationCoefficient.model_validate(
#         attenuation_coefficient,
#         from_attributes=True,
#     )


# @router.post(
#     "",
#     response_model=schemas.AttenuationCoefficient,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_attenuation_coefficient(
#     material: schemas.AttenuationCoefficientCreate,
#     db=Depends(get_db),
# ) -> schemas.AttenuationCoefficient:
#     attenuation_coefficient = crud.create_attenuation_coefficient(
#         db=db,
#         attenuation_coefficient=attenuation_coefficient,
#     )

#     if attenuation_coefficient is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Attenuation Coefficient not found.",
#         )

#     return schemas.AttenuationCoefficient.model_validate(
#         attenuation_coefficient,
#         from_attributes=True,
#     )


# @router.patch(
#     "/{attenuation_coefficient_id}",
#     response_model=schemas.AttenuationCoefficient,
#     status_code=status.HTTP_200_OK,
# )
# def update_attenuation_coefficient(
#     attenuation_coefficient_id: int,
#     attenuation_coefficient: schemas.AttenuationCoefficientUpdate,
#     db=Depends(get_db),
# ) -> schemas.AttenuationCoefficient:
#     attenuation_coefficient = crud.update_attenuation_coefficient(
#         db=db,
#         attenuation_coefficient_id=attenuation_coefficient_id,
#         attenuation_coefficient=attenuation_coefficient,
#     )

#     if attenuation_coefficient is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Attenuation Coefficient not found.",
#         )

#     return schemas.AttenuationCoefficient.model_validate(
#         attenuation_coefficient,
#         from_attributes=True,
#     )


# @router.delete(
#     "/{attenuation_coefficient_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# def delete_attenuation_coefficient(
#     attenuation_coefficient_id: int,
#     db=Depends(get_db),
# ):
#     crud.delete_attenuation_coefficient(
#         db=db, attenuation_coefficient_id=attenuation_coefficient_id
#     )
