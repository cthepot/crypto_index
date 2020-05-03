"""removed asset_id

Revision ID: 8d51f26d3c6c
Revises: 85025d9c171e
Create Date: 2020-03-21 15:08:10.556594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d51f26d3c6c'
down_revision = '85025d9c171e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('index_asset_id_fkey', 'index', type_='foreignkey')
    op.drop_column('index', 'asset_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('index', sa.Column('asset_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('index_asset_id_fkey', 'index', 'asset', ['asset_id'], ['id'])
    # ### end Alembic commands ###
