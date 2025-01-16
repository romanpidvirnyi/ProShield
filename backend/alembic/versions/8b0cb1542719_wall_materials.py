"""wall materials

Revision ID: 8b0cb1542719
Revises: eeb179a68b33
Create Date: 2025-01-16 23:01:26.187389

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8b0cb1542719"
down_revision: Union[str, None] = "eeb179a68b33"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "wall_materials",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_wall_materials")),
        sa.UniqueConstraint("name", name=op.f("uq_wall_materials_name")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("wall_materials")
    # ### end Alembic commands ###