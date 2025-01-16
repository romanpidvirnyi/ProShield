from typing import TYPE_CHECKING, Optional

from proshield.db.models.base import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from proshield.db.models import BuildingType, WallMaterial


class BuildingCoefficient(Base):
    __tablename__ = "building_coefficients"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Матеріал стін
    wall_material_id: Mapped[int] = mapped_column(ForeignKey("wall_materials.id"))
    # Характер забудови
    building_type_id: Mapped[int] = mapped_column(ForeignKey("building_types.id"))
    # товщина стін
    wall_thickness: Mapped[int] = mapped_column()
    # Вага
    weight: Mapped[int] = mapped_column()
    # Площа отворів по відношенню до площі огороджувальних конструкцій будинків
    area_relation_percent: Mapped[int] = mapped_column()
    # Коефіцієнт
    coefficient: Mapped[float] = mapped_column()

    building_type: Mapped["BuildingType"] = relationship(
        "BuildingType",
        foreign_keys="BuildingCoefficient.building_type_id",
    )
    wall_material: Mapped["WallMaterial"] = relationship(
        "WallMaterial",
        foreign_keys="BuildingCoefficient.wall_material_id",
    )

    @property
    def building_type_name(self) -> str:
        return self.building_type.name

    @property
    def wall_material_name(self) -> str:
        return self.wall_material.name
