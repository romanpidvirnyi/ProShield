from typing import TYPE_CHECKING

from proshield.db.models.base import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from proshield.db.models import LocationConditionCoefficient


class BuildingType(Base):
    __tablename__ = "building_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    coefficients: Mapped[list["LocationConditionCoefficient"]] = relationship(
        "LocationConditionCoefficient",
        back_populates="building_type",
    )
