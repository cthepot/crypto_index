"""added index.asset_id array of integer

Revision ID: 96a875d6f0d4
Revises: 8d51f26d3c6c
Create Date: 2020-03-21 15:08:43.520305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96a875d6f0d4'
down_revision = '8d51f26d3c6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('index', sa.Column('asset_id', sa.ARRAY(sa.Integer()), nullable=True))
    op.create_foreign_key(None, 'index', 'asset', ['asset_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'index', type_='foreignkey')
    op.drop_column('index', 'asset_id')
    # ### end Alembic commands ###
