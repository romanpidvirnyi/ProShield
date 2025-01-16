from typing import Optional

from pydantic import BaseModel


class LocationConditionCoefficientCreate(BaseModel):
    building_type_id: int
    building_height_from: Optional[int] = None
    building_height_to: Optional[int] = None
    building_density: int
    coefficient: float


class LocationConditionCoefficient(LocationConditionCoefficientCreate):
    id: int
    building_type_name: str


class LocationConditionCoefficientUpdate(BaseModel):
    coefficient: Optional[float] = None
