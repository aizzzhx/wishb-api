"""Fix ExchangeStatus Enum issue

Revision ID: 67a338a0fe6d
Revises: 985dc3f2933d
Create Date: 2024-10-27 22:07:55.886662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67a338a0fe6d'
down_revision: Union[str, None] = '985dc3f2933d'
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
