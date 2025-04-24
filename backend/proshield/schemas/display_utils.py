from pydantic import BaseModel


class MaterialDisplay(BaseModel):
    id: int
    name: str


class SubMaterialDisplay(BaseModel):
    id: int
    name: str
    density: float
    display_name: str
    coefficients: list["SubMaterialCoefficientDisplay"]
    minimum_thickness: int
    maximum_thickness: int


class SubMaterialCoefficientDisplay(BaseModel):
    id: int
    thickness: int
    coefficient: float
