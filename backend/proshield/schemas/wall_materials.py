from pydantic import BaseModel


class WallMaterialCreate(BaseModel):
    name: str


class WallMaterial(WallMaterialCreate):
    id: int


class WallMaterialUpdate(WallMaterialCreate):
    pass
