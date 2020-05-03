"""create table

Revision ID: f2cb84d61325
Revises: 
Create Date: 2020-03-20 01:01:32.101824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2cb84d61325'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('asset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('assetname', sa.String(length=120), nullable=True),
    sa.Column('slug', sa.String(length=48), nullable=True),
    sa.Column('symbol', sa.String(length=10), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.Column('first_historical_data', sa.DateTime(), nullable=True),
    sa.Column('last_historical_data', sa.DateTime(), nullable=True),
    sa.Column('platform', sa.String(length=120), nullable=True),
    sa.Column('id_cmc', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('rank')
    )
    op.create_index(op.f('ix_asset_assetname'), 'asset', ['assetname'], unique=True)
    op.create_index(op.f('ix_asset_id_cmc'), 'asset', ['id_cmc'], unique=True)
    op.create_index(op.f('ix_asset_slug'), 'asset', ['slug'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('index',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('asset_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['asset.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_index_timestamp'), 'index', ['timestamp'], unique=False)
    op.create_table('quote',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_cmc', sa.Integer(), nullable=True),
    sa.Column('assetname', sa.String(length=120), nullable=True),
    sa.Column('symbol', sa.String(length=10), nullable=True),
    sa.Column('slug', sa.String(length=48), nullable=True),
    sa.Column('num_market_pairs', sa.Integer(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('tags', sa.PickleType(), nullable=True),
    sa.Column('max_supply', sa.Float(), nullable=True),
    sa.Column('circulating_supply', sa.Float(), nullable=True),
    sa.Column('total_supply', sa.Float(), nullable=True),
    sa.Column('platform', sa.PickleType(), nullable=True),
    sa.Column('price_usd', sa.Float(), nullable=True),
    sa.Column('volume_24h_usd', sa.Float(), nullable=True),
    sa.Column('percent_change_1h_usd', sa.Float(), nullable=True),
    sa.Column('percent_change_24h_usd', sa.Float(), nullable=True),
    sa.Column('percent_change_7d_usd', sa.Float(), nullable=True),
    sa.Column('market_cap_usd', sa.Float(), nullable=True),
    sa.Column('last_updated_usd', sa.DateTime(), nullable=True),
    sa.Column('asset_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['asset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quote_assetname'), 'quote', ['assetname'], unique=False)
    op.create_index(op.f('ix_quote_id_cmc'), 'quote', ['id_cmc'], unique=False)
    op.create_index(op.f('ix_quote_num_market_pairs'), 'quote', ['num_market_pairs'], unique=False)
    op.create_index(op.f('ix_quote_slug'), 'quote', ['slug'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_quote_slug'), table_name='quote')
    op.drop_index(op.f('ix_quote_num_market_pairs'), table_name='quote')
    op.drop_index(op.f('ix_quote_id_cmc'), table_name='quote')
    op.drop_index(op.f('ix_quote_assetname'), table_name='quote')
    op.drop_table('quote')
    op.drop_index(op.f('ix_index_timestamp'), table_name='index')
    op.drop_table('index')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_asset_slug'), table_name='asset')
    op.drop_index(op.f('ix_asset_id_cmc'), table_name='asset')
    op.drop_index(op.f('ix_asset_assetname'), table_name='asset')
    op.drop_table('asset')
    # ### end Alembic commands ###
