from app import crud, schemas
from app.core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="")


@router.get(
    "",
    response_model=list[schemas.Material],
    status_code=status.HTTP_200_OK,
)
def get_materials(db=Depends(get_db)) -> list[schemas.Material]:
    materials = crud.get_materials(db=db)
    return [
        schemas.Material.model_validate(
            material,
            from_attributes=True,
        )
        for material in materials
    ]


@router.get(
    "/{material_id}",
    response_model=schemas.Material,
    status_code=status.HTTP_200_OK,
)
def get_material(
    material_id: int,
    db=Depends(get_db),
) -> schemas.Material:
    material = crud.get_material_by_id(
        db=db,
        material_id=material_id,
    )

    if material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found.",
        )

    return schemas.Material.model_validate(
        material,
        from_attributes=True,
    )


@router.post(
    "",
    response_model=schemas.Material,
    status_code=status.HTTP_201_CREATED,
)
def create_material(
    material: schemas.MaterialCreate,
    db=Depends(get_db),
) -> schemas.Material:
    material = crud.create_material(
        db=db,
        material=material,
    )

    if material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found.",
        )

    return schemas.Material.model_validate(
        material,
        from_attributes=True,
    )


@router.patch(
    "/{material_id}",
    response_model=schemas.Material,
    status_code=status.HTTP_200_OK,
)
def update_material(
    material_id: int,
    material: schemas.MaterialUpdate,
    db=Depends(get_db),
) -> schemas.MaterialUpdate:
    material = crud.update_material(db=db, material_id=material_id, material=material)

    if material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found.",
        )

    return schemas.Material.model_validate(
        material,
        from_attributes=True,
    )


@router.delete(
    "/{material_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_material(
    material_id: int,
    db=Depends(get_db),
):
    crud.delete_material(db=db, material_id=material_id)
