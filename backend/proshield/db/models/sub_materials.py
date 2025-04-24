from typing import TYPE_CHECKING

from proshield.db.models.base import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from proshield.db.models.materials import Material


class SubMaterial(Base):
    __tablename__ = "sub_materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"))
    name: Mapped[str] = mapped_column()
    density: Mapped[float] = mapped_column(default=0.0)

    __table_args__ = (UniqueConstraint("material_id", "name", "density"),)

    material: Mapped["Material"] = relationship(
        "Material",
        back_populates="sub_materials",
        foreign_keys="SubMaterial.material_id",
    )

    coefficients: Mapped[list["SubMaterialCoefficient"]] = relationship(
        "SubMaterialCoefficient",
        back_populates="sub_material",
    )

    @property
    def display_name(self) -> str:
        return f"{self.name} ({self.density} г/см3)"

    @property
    def minimum_thickness(self) -> int:
        if not self.coefficients:
            return 0
        return min(coefficient.thickness for coefficient in self.coefficients)

    @property
    def maximum_thickness(self) -> int:
        if not self.coefficients:
            return 0
        return max(coefficient.thickness for coefficient in self.coefficients)


class SubMaterialCoefficient(Base):
    __tablename__ = "sub_material_coefficients"

    id: Mapped[int] = mapped_column(primary_key=True)
    sub_material_id: Mapped[int] = mapped_column(ForeignKey("sub_materials.id"))
    thickness: Mapped[int] = mapped_column()
    coefficient: Mapped[float] = mapped_column()

    sub_material: Mapped["SubMaterial"] = relationship(
        "SubMaterial",
        back_populates="coefficients",
        foreign_keys="SubMaterialCoefficient.sub_material_id",
    )
