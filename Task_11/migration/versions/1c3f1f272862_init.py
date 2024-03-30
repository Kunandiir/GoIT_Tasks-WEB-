"""Init

Revision ID: 1c3f1f272862
Revises: 7de4b537bd7d
Create Date: 2024-03-29 14:42:27.870054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c3f1f272862'
down_revision: Union[str, None] = '7de4b537bd7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('first_name', sa.String(length=50), nullable=True))
    op.drop_column('contact', 'fullname')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('fullname', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column('contact', 'first_name')
    # ### end Alembic commands ###
