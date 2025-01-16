from pydantic import BaseModel


class BuildingTypeCreate(BaseModel):
    name: str


class BuildingType(BuildingTypeCreate):
    id: int


class BuildingTypeUpdate(BuildingTypeCreate):
    pass
