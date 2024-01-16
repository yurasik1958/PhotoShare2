"""add unique

Revision ID: 1e30e1962637
Revises: 5234890086c5
Create Date: 2023-10-21 21:45:58.998957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e30e1962637'
down_revision: Union[str, None] = '5234890086c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uq_tag_m2m_photo', 'tag_m2m_photo', ['tag_id', 'photo_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_tag_m2m_photo', 'tag_m2m_photo', type_='unique')
    # ### end Alembic commands ###