from proshield.schemas.display_utils import (
    MaterialDisplay,
    SubMaterialCoefficientDisplay,
)
from pydantic import BaseModel


class SubMaterialCreate(BaseModel):
    material_id: int
    name: str
    density: float = 0.0


class SubMaterial(SubMaterialCreate):
    id: int
    display_name: str
    minimum_thickness: int
    maximum_thickness: int
    material: MaterialDisplay
    coefficients: list[SubMaterialCoefficientDisplay]


class SubMaterialUpdate(SubMaterialCreate):
    pass
