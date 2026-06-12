"""create ho so lich su

Revision ID: 004
Revises: 003
Create Date: 2026-06-12 12:03:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('ho_so_lich_su',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ho_so_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('nguoi_thuc_hien_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('hanh_dong', sa.String(length=50), nullable=False),
        sa.Column('trang_thai_cu', sa.String(length=30), nullable=True),
        sa.Column('trang_thai_moi', sa.String(length=30), nullable=True),
        sa.Column('ghi_chu', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['ho_so_id'], ['ho_so.id'], ),
        sa.ForeignKeyConstraint(['nguoi_thuc_hien_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('ho_so_lich_su')
