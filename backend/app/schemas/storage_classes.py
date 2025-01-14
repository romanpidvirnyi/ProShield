from typing import Optional

from pydantic import BaseModel


class StorageClassCreate(BaseModel):
    description: str
    protection_class: str
    overpressure_air_blast_wave: int
    radiation_protection_level: int


class StorageClass(StorageClassCreate):
    id: int


class StorageClassUpdate(BaseModel):
    description: Optional[str] = None
    protection_class: Optional[str] = None
    overpressure_air_blast_wave: Optional[int] = None
    radiation_protection_level: Optional[int] = None
