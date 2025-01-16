from typing import TYPE_CHECKING

from proshield.db.models.base import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from proshield.db.models import Material


class AttenuationCoefficient(Base):
    """
    Табоиця коефіцієнтів послаблення дози гамма-випромінювання
    та нейтронів проникаючої радіації товщею матеріалів
    """

    __tablename__ = "attenuation_coefficients"

    id: Mapped[int] = mapped_column(primary_key=True)
    # матеріал
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"))
    # товщина шару матеріалу
    material_thickness: Mapped[int] = mapped_column()
    # щільність матеріалу
    material_density: Mapped[float] = mapped_column()
    # коефіцієнт послаблення дози нейтронів огороджувальною конструкцією
    neutron_dose_coefficient: Mapped[float] = mapped_column()
    # коефіцієнт послаблення дози гамма-випромінювання огороджувальною конструкцією
    gamma_dose_coefficient: Mapped[float] = mapped_column()

    material: Mapped["Material"] = relationship(
        "Material",
        foreign_keys="AttenuationCoefficient.material_id",
    )

    @property
    def material_name(self) -> str:
        return self.material.name
