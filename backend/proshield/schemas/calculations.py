from pydantic import BaseModel


class MeterialThickness(BaseModel):
    material_id: int
    thickness: int


class CalculateAZF(BaseModel):
    # coefficient zab
    building_type_id: int
    building_height: str
    building_density: int
    # coefficient bud
    wall_material_id: int
    wall_material_thickness: int
    area_relation_percent: int
    # coefficient az
    storage_class_id: int

    materials: list[MeterialThickness]


class AZFResults(BaseModel):
    az: float
    kzab: float
    kbud: float
    ky: float
    kn: float
    KN: float
    AZF: float
