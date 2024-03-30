"""New Migration

Revision ID: 6b8ca91c6925
Revises: ac9b17722d9e
Create Date: 2024-03-29 12:50:07.114981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b8ca91c6925'
down_revision: Union[str, None] = 'ac9b17722d9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'contact',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('fullname', sa.String(length=50), nullable=True),
        sa.Column('last_name', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column('birthday', sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('contact')
