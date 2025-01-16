from typing import Optional

from pydantic import BaseModel


class BuildingCoefficientCreate(BaseModel):
    wall_material_id: int
    building_type_id: int
    wall_thickness: int
    weight: int
    area_relation_percent: int
    coefficient: float


class BuildingCoefficient(BuildingCoefficientCreate):
    id: int
    building_type_name: str
    wall_material_name: str


class BuildingCoefficientUpdate(BaseModel):
    coefficient: Optional[float] = None
