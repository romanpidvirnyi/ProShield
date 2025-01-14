from app.db.models.base import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class StorageClass(Base):
    __tablename__ = "storage_classes"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column()
    protection_class: Mapped[str] = mapped_column(unique=True)
    overpressure_air_blast_wave: Mapped[int] = mapped_column()
    radiation_protection_level: Mapped[int] = mapped_column()
