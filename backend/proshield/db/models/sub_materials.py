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

    @property
    def display_name(self) -> str:
        return f"{self.name} ({self.density} г/см3)"
