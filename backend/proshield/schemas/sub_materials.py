from proshield.schemas.display_utils import MaterialDisplay
from pydantic import BaseModel


class SubMaterialCreate(BaseModel):
    material_id: int
    name: str
    density: float = 0.0


class SubMaterial(SubMaterialCreate):
    id: int
    display_name: str

    material: MaterialDisplay


class SubMaterialUpdate(SubMaterialCreate):
    pass
