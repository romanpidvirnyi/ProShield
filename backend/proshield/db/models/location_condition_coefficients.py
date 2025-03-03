from typing import TYPE_CHECKING, Optional

from proshield.db.models.base import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from proshield.db.models import BuildingType


class LocationConditionCoefficient(Base):
    __tablename__ = "location_condition_coefficients"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Характер забудови
    building_type_id: Mapped[int] = mapped_column(ForeignKey("building_types.id"))
    # Висота будинків
    building_height: Mapped[str] = mapped_column(nullable=True)
    # Щільність забудови
    building_density: Mapped[int] = mapped_column()
    # Коефіцієнт
    coefficient: Mapped[float] = mapped_column()

    building_type: Mapped["BuildingType"] = relationship(
        "BuildingType",
        foreign_keys="LocationConditionCoefficient.building_type_id",
    )

    @property
    def building_type_name(self) -> str:
        return self.building_type.name
