from proshield.schemas.display_utils import SubMaterialDisplay
from pydantic import BaseModel


class MaterialCreate(BaseModel):
    name: str


class Material(MaterialCreate):
    id: int
    sub_materials: list[SubMaterialDisplay]


class MaterialUpdate(MaterialCreate):
    pass
