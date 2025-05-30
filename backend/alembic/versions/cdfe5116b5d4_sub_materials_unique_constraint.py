"""sub-materials unique constraint

Revision ID: cdfe5116b5d4
Revises: 9a7e1393479c
Create Date: 2025-04-24 06:41:03.285523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdfe5116b5d4'
down_revision: Union[str, None] = '9a7e1393479c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_sub_materials_name', 'sub_materials', type_='unique')
    op.create_unique_constraint(op.f('uq_sub_materials_material_id'), 'sub_materials', ['material_id', 'name', 'density'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_sub_materials_material_id'), 'sub_materials', type_='unique')
    op.create_unique_constraint('uq_sub_materials_name', 'sub_materials', ['name'])
    # ### end Alembic commands ###
