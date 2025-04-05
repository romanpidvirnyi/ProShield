from fastapi import APIRouter, Depends, HTTPException, status
from proshield import crud, schemas
from proshield.core.database import get_db

router = APIRouter(prefix="")


@router.get(
    "",
    response_model=list[schemas.StorageClass],
    status_code=status.HTTP_200_OK,
)
def get_starage_classes(db=Depends(get_db)) -> list[schemas.StorageClass]:
    storage_classes = crud.get_storage_classes(db=db)
    return [
        schemas.StorageClass.model_validate(
            storage_class,
            from_attributes=True,
        )
        for storage_class in storage_classes
    ]


# @router.get(
#     "/{storage_class_id}",
#     response_model=schemas.StorageClass,
#     status_code=status.HTTP_200_OK,
# )
# def get_starage_class(
#     storage_class_id: int,
#     db=Depends(get_db),
# ) -> schemas.StorageClass:
#     storage_class = crud.get_storage_class_by_id(
#         db=db,
#         storage_class_id=storage_class_id,
#     )

#     if storage_class is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Storage Class not found.",
#         )

#     return schemas.StorageClass.model_validate(
#         storage_class,
#         from_attributes=True,
#     )


# @router.post(
#     "",
#     response_model=schemas.StorageClass,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_starage_class(
#     storage_class: schemas.StorageClassCreate,
#     db=Depends(get_db),
# ) -> schemas.StorageClass:
#     storage_class = crud.create_storage_class(
#         db=db,
#         storage_class=storage_class,
#     )

#     if storage_class is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Storage Class not found.",
#         )

#     return schemas.StorageClass.model_validate(
#         storage_class,
#         from_attributes=True,
#     )


# @router.patch(
#     "/{storage_class_id}",
#     response_model=schemas.StorageClass,
#     status_code=status.HTTP_200_OK,
# )
# def update_starage_class(
#     storage_class_id: int,
#     storage_class: schemas.StorageClassUpdate,
#     db=Depends(get_db),
# ) -> schemas.StorageClass:
#     storage_class = crud.update_storage_class(
#         db=db,
#         storage_class_id=storage_class_id,
#         storage_class=storage_class,
#     )

#     if storage_class is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Storage Class not found.",
#         )

#     return schemas.StorageClass.model_validate(
#         storage_class,
#         from_attributes=True,
#     )


# @router.delete(
#     "/{storage_class_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# def delete_starage_class(
#     storage_class_id: int,
#     db=Depends(get_db),
# ):
#     crud.delete_storage_class(
#         db=db,
#         storage_class_id=storage_class_id,
#     )
