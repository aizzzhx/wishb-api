"""add description to users

Revision ID: 5eebced5ce74
Revises: bf85e0289ac0
Create Date: 2024-10-20 11:37:29.506889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5eebced5ce74'
down_revision: Union[str, None] = 'bf85e0289ac0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'description')
    # ### end Alembic commands ###