"""Added Book and BookCondition models

Revision ID: 985dc3f2933d
Revises: 5eebced5ce74
Create Date: 2024-10-20 12:30:45.508635

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '985dc3f2933d'
down_revision: Union[str, None] = '5eebced5ce74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###