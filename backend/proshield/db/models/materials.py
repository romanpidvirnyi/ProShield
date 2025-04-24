from typing import TYPE_CHECKING

from proshield.db.models.base import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from proshield.db.models.sub_materials import SubMaterial


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    sub_materials: Mapped[list["SubMaterial"]] = relationship(
        "SubMaterial",
        back_populates="material",
    )
