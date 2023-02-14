"""add user table

Revision ID: aa49dd0431ab
Revises: 5968e05ef02e
Create Date: 2023-02-14 09:25:27.926144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa49dd0431ab'
down_revision = '5968e05ef02e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('email', sa.String, nullable=False),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
