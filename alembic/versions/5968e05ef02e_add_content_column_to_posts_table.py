"""add content column to posts table

Revision ID: 5968e05ef02e
Revises: 622dc8e3b57c
Create Date: 2023-02-14 09:16:07.160376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5968e05ef02e'
down_revision = '622dc8e3b57c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
