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
    # KN roof
    KN_ROOF = None
    for item in data.roof_materials:
        sub_material_coefficient = crud.get_sub_material_coefficient_by_params(
            db=db,
            sub_material_id=item.sub_material_id,
            thickness=item.thickness,
        )
        if sub_material_coefficient is not None:
            if KN_ROOF is None:
                KN_ROOF = sub_material_coefficient.coefficient
            elif KN_ROOF < sub_material_coefficient.coefficient:
                KN_ROOF = sub_material_coefficient.coefficient

    # KN wall
    KN_WALL = None
    for item in data.wall_materials:
        sub_material_coefficient = crud.get_sub_material_coefficient_by_params(
            db=db,
            sub_material_id=item.sub_material_id,
            thickness=item.thickness,
        )
        if sub_material_coefficient is not None:
            if KN_WALL is None:
                KN_WALL = sub_material_coefficient.coefficient
            elif KN_WALL < sub_material_coefficient.coefficient:
                KN_WALL = sub_material_coefficient.coefficient

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
    attenuation_coefficients_wall = []
    for item in data.wall_materials:
        attenuation_coefficients_wall.append(
            crud.get_attenuation_coefficient_by_params(
                db=db,
                material_id=item.material_id,
                material_thickness=item.thickness,
            )
        )

    attenuation_coefficients_roof = []
    for item in data.roof_materials:
        attenuation_coefficients_roof.append(
            crud.get_attenuation_coefficient_by_params(
                db=db,
                material_id=item.material_id,
                material_thickness=item.thickness,
            )
        )

    ky_wall = 1
    for item in attenuation_coefficients_wall:
        ky_wall *= item.gamma_dose_coefficient

    ky_roof = 1
    for item in attenuation_coefficients_roof:
        ky_roof *= item.gamma_dose_coefficient

    kn_wall = 1
    for item in attenuation_coefficients_wall:
        kn_wall *= item.neutron_dose_coefficient

    kn_roof = 1
    for item in attenuation_coefficients_roof:
        kn_roof *= item.neutron_dose_coefficient

    Azf_roof = (
        1.18 * (ky_roof * kn_roof) * (kzab / kbud) * KN_ROOF / (ky_roof + kn_roof)
    )
    Azf_wall = (
        1.18 * (ky_wall * kn_wall) * (kzab / kbud) * KN_WALL / (ky_wall + kn_wall)
    )

    return schemas.AZFResults(
        az=az,
        kzab=kzab,
        kbud=kbud,
        ky_roof=ky_roof,
        kn_roof=kn_roof,
        ky_wall=ky_wall,
        kn_wall=kn_wall,
        KN_ROOF=KN_ROOF,
        AZF_ROOF=Azf_roof,
        KN_WALL=KN_WALL,
        AZF_WALL=Azf_wall,
    )
