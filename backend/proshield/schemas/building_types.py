from proshield.schemas.display_utils import LocationConditionCoefficientDisplay
from pydantic import BaseModel


class BuildingTypeCreate(BaseModel):
    name: str


class BuildingType(BuildingTypeCreate):
    id: int
    coefficients: list[LocationConditionCoefficientDisplay]


class BuildingTypeUpdate(BuildingTypeCreate):
    pass
