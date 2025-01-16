"""location condition coefficients

Revision ID: eeb179a68b33
Revises: 0736ea225068
Create Date: 2025-01-16 22:16:09.888981

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "eeb179a68b33"
down_revision: Union[str, None] = "0736ea225068"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "location_condition_coefficients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("building_type_id", sa.Integer(), nullable=False),
        sa.Column("building_height_from", sa.Integer(), nullable=True),
        sa.Column("building_height_to", sa.Integer(), nullable=True),
        sa.Column("building_density", sa.Integer(), nullable=False),
        sa.Column("coefficient", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["building_type_id"],
            ["building_types.id"],
            name=op.f(
                "fk_location_condition_coefficients_building_type_id_building_types"
            ),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_location_condition_coefficients")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("location_condition_coefficients")
    # ### end Alembic commands ###
