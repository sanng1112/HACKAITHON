"""create ho so tai lieu

Revision ID: 003
Revises: 002
Create Date: 2026-06-12 12:02:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('ho_so_tai_lieu',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ho_so_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ten_file', sa.String(length=255), nullable=False),
        sa.Column('duong_dan', sa.Text(), nullable=False),
        sa.Column('loai_file', sa.String(length=50), nullable=False),
        sa.Column('kich_thuoc', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['ho_so_id'], ['ho_so.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('ho_so_tai_lieu')
