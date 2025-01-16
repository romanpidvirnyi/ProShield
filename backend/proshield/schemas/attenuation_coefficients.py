from typing import Optional

from pydantic import BaseModel


class AttenuationCoefficientCreate(BaseModel):
    material_id: int
    material_thickness: int
    material_density: float
    neutron_dose_coefficient: float
    gamma_dose_coefficient: float


class AttenuationCoefficient(AttenuationCoefficientCreate):
    id: int
    material_name: str


class AttenuationCoefficientUpdate(BaseModel):
    neutron_dose_coefficient: Optional[float] = None
    gamma_dose_coefficient: Optional[float] = None
