"""add foreign key to posts table

Revision ID: 224dbaf13622
Revises: aa49dd0431ab
Create Date: 2023-02-14 11:59:20.154782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '224dbaf13622'
down_revision = 'aa49dd0431ab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'],
                          remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
