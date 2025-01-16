from fastapi import APIRouter, Depends, HTTPException, status
from proshield import crud, schemas
from proshield.core.database import get_db

router = APIRouter(prefix="")


@router.get(
    "",
    response_model=list[schemas.Material],
    status_code=status.HTTP_200_OK,
)
def get_wall_materials(db=Depends(get_db)) -> list[schemas.WallMaterial]:
    materials = crud.get_wall_materials(db=db)
    return [
        schemas.WallMaterial.model_validate(
            material,
            from_attributes=True,
        )
        for material in materials
    ]


@router.get(
    "/{material_id}",
    response_model=schemas.WallMaterial,
    status_code=status.HTTP_200_OK,
)
def get_wall_material(
    material_id: int,
    db=Depends(get_db),
) -> schemas.WallMaterial:
    material = crud.get_wall_material_by_id(
        db=db,
        material_id=material_id,
    )

    if material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found.",
        )

    return schemas.WallMaterial.model_validate(
        material,
        from_attributes=True,
    )


@router.post(
    "",
    response_model=schemas.Material,
    status_code=status.HTTP_201_CREATED,
)
def create_wall_material(
    material: schemas.WallMaterialCreate,
    db=Depends(get_db),
) -> schemas.WallMaterial:
    material = crud.create_wall_material(
        db=db,
        material=material,
    )

    if material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found.",
        )

    return schemas.WallMaterial.model_validate(
        material,
        from_attributes=True,
    )


@router.patch(
    "/{material_id}",
    response_model=schemas.WallMaterial,
    status_code=status.HTTP_200_OK,
)
def update_wall_material(
    material_id: int,
    material: schemas.WallMaterialUpdate,
    db=Depends(get_db),
) -> schemas.MaterialUpdate:
    material = crud.update_wall_material(
        db=db, material_id=material_id, material=material
    )

    if material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found.",
        )

    return schemas.WallMaterial.model_validate(
        material,
        from_attributes=True,
    )


@router.delete(
    "/{material_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_material(
    material_id: int,
    db=Depends(get_db),
):
    crud.delete_wall_material(db=db, material_id=material_id)
