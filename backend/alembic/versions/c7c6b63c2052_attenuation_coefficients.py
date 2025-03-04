"""attenuation_coefficients

Revision ID: c7c6b63c2052
Revises: 714b9a13b3e0
Create Date: 2025-01-14 22:38:05.756662

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c7c6b63c2052"
down_revision: Union[str, None] = "714b9a13b3e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "attenuation_coefficients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("material_id", sa.Integer(), nullable=False),
        sa.Column("material_thickness", sa.Integer(), nullable=False),
        sa.Column("material_density", sa.Float(), nullable=False),
        sa.Column("neutron_dose_coefficient", sa.Float(), nullable=False),
        sa.Column("gamma_dose_coefficient", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["material_id"],
            ["materials.id"],
            name=op.f("fk_attenuation_coefficients_material_id_materials"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_attenuation_coefficients")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("attenuation_coefficients")
    # ### end Alembic commands ###
