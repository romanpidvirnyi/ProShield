from pydantic import BaseModel


class MaterialDisplay(BaseModel):
    id: int
    name: str


class SubMaterialDisplay(BaseModel):
    id: int
    name: str
    density: float
    display_name: str
