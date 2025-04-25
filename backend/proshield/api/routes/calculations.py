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
    az = data.az
    # KN
    KN = None
    for item in data.materials:
        sub_material_coefficient = crud.get_sub_material_coefficient_by_params(
            db=db,
            sub_material_id=item.sub_material_id,
            thickness=item.thickness,
        )
        if sub_material_coefficient is not None:
            if KN is None:
                KN = sub_material_coefficient.coefficient
            elif KN < sub_material_coefficient.coefficient:
                KN = sub_material_coefficient.coefficient

    # kbud
    kbud = data.coefficient_bud

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
