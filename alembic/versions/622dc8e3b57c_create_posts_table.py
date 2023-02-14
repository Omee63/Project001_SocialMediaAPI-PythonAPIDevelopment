"""Create Posts Table

Revision ID: 622dc8e3b57c
Revises: 
Create Date: 2023-02-13 22:02:07.646744

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '622dc8e3b57c'
down_revision = None
branch_labels = None
depends_on = None


# we have to do both of the functions manually.
# in 'upgrade' function, we write all the logics to perform update in the database tables
# 'upgrade' function handles database update operations
def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False))
    pass


# in 'downgrade' function, we write all the logics to perform rollback operation in the database tables if we want to.
# 'downgrade' function handles database rollback operations
def downgrade():
    op.drop_table('posts')
    pass
