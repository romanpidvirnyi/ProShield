from typing import Optional

from pydantic import BaseModel


class MeterialThickness(BaseModel):
    material_id: int
    sub_material_id: int
    thickness: int


class CalculateAZF(BaseModel):
    # coefficient az
    az: int
    # coefficient zab
    building_type_id: int
    building_height: str
    building_density: int
    # coefficient bud
    coefficient_bud: Optional[int] = 1

    materials: list[MeterialThickness]


class AZFResults(BaseModel):
    az: float
    kzab: float
    kbud: float
    ky: float
    kn: float
    KN: float
    AZF: float
