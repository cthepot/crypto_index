"""IndexAsset.asset_id foreign key from Asset.id to Asset.id_cmc

Revision ID: bc8215a90df8
Revises: b628540fb548
Create Date: 2020-03-25 11:47:21.304974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc8215a90df8'
down_revision = 'b628540fb548'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('index_asset_asset_id_fkey', 'index_asset', type_='foreignkey')
    op.create_foreign_key(None, 'index_asset', 'asset', ['asset_id'], ['id_cmc'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'index_asset', type_='foreignkey')
    op.create_foreign_key('index_asset_asset_id_fkey', 'index_asset', 'asset', ['asset_id'], ['id'])
    # ### end Alembic commands ###