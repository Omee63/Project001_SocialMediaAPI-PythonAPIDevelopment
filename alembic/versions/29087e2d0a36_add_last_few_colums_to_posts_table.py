"""add last few colums to posts table

Revision ID: 29087e2d0a36
Revises: 224dbaf13622
Create Date: 2023-02-14 12:08:46.578750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29087e2d0a36'
down_revision = '224dbaf13622'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at',
                                     sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
