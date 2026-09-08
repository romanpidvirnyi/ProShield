from typing import Optional

from pydantic import BaseModel


class MeterialThickness(BaseModel):
    material_id: int
    sub_material_id: int
    thickness: int


class CalculateAZF(BaseModel):
    # coefficient az
    az: int
    # coefficient zab
    building_type_id: int
    building_height: str
    building_density: int
    # coefficient bud
    coefficient_bud_wall: Optional[float] = 1.0
    coefficient_bud_roof: Optional[float] = 1.0

    roof_materials: list[MeterialThickness]
    wall_materials: list[MeterialThickness]


class AZFResults(BaseModel):
    az: float
    kzab: float
    coefficient_bud_wall: float
    coefficient_bud_roof: float
    ky_wall: float
    kn_wall: float
    ky_roof: float
    kn_roof: float
    KN_ROOF: float
    KN_WALL: float
    AZF_ROOF: float
    AZF_WALL: float


class MaterialDisplay(BaseModel):
    material: str
    submaterial: str
    thickness: int


class BuildingWallDisplay(BaseModel):
    material: str
    thickness: str
    openings_percent: int


class PDFDownloadRequest(BaseModel):
    az: float
    shelter_class_name: str
    wall_materials: list[MaterialDisplay]
    roof_materials: list[MaterialDisplay]
    building_type_name: str
    building_height: str
    building_density: int
    building_wall_params: Optional[BuildingWallDisplay] = None
    kzab: float
    coefficient_bud_wall: float
    coefficient_bud_roof: float
    ky_wall: float
    kn_wall: float
    ky_roof: float
    kn_roof: float
    KN_WALL: float
    KN_ROOF: float
    AZF_WALL: float
    AZF_ROOF: float
