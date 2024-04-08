"""add table users

Revision ID: ec4181f0a450
Revises: 1c3f1f272862
Create Date: 2024-03-31 21:41:09.368529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec4181f0a450'
down_revision: Union[str, None] = '1c3f1f272862'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('avatar', sa.String(length=250), nullable=True),
    sa.Column('refresh_token', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.add_column('contact', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('contact', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('contact', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'contact', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'contact', type_='foreignkey')
    op.drop_column('contact', 'user_id')
    op.drop_column('contact', 'updated_at')
    op.drop_column('contact', 'created_at')
    op.drop_table('users')
    # ### end Alembic commands ###