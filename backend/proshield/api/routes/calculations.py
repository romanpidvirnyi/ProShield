from fastapi import APIRouter, Depends, HTTPException, status
from proshield import crud, schemas
from proshield.core.database import get_db

router = APIRouter(prefix="")


@router.post(
    "/azf",
    response_model=schemas.AZFResults,
    status_code=status.HTTP_200_OK,
)
def calculate_az(
    data: schemas.CalculateAZF,
    db=Depends(get_db),
) -> schemas.AZFResults:
    # az
    az = crud.get_storage_class_by_id(db=db, storage_class_id=data.storage_class_id)
    if az is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Storage Class not found.",
        )
    az = az.radiation_protection_level
    # kzab
    kzab = crud.get_location_condition_coefficient_by_params(
        db=db,
        building_type_id=data.building_type_id,
        building_height=data.building_height,
        building_density=data.building_density,
    )
    if kzab is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location Condition Coefficient not found.",
        )
    kzab = kzab.coefficient
    # kbud
    kbud = crud.get_building_coefficient_by_params(
        db=db,
        building_type_id=data.building_type_id,
        wall_material_id=data.wall_material_id,
        wall_thickness=data.wall_material_thickness,
        area_relation_percent=data.area_relation_percent,
    )
    if kbud is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building Coefficient not found.",
        )
    kbud = kbud.coefficient

    # attenuation_coefficients
    attenuation_coefficients = []
    for item in data.materials:
        attenuation_coefficients.append(
            crud.get_attenuation_coefficient_by_params(
                db=db,
                material_id=item.material_id,
                material_thickness=item.thickness,
            )
        )

    ky = 1
    for item in attenuation_coefficients:
        ky *= item.gamma_dose_coefficient

    kn = 1
    for item in attenuation_coefficients:
        kn *= item.neutron_dose_coefficient

    KN = 1.4

    Azf = 1.18 * (ky * kn) * (kzab / kbud) * KN / (ky + kn)
    return schemas.AZFResults(
        az=az,
        kzab=kzab,
        kbud=kbud,
        ky=ky,
        kn=kn,
        KN=KN,
        AZF=Azf,
    )
