"""create lich hen

Revision ID: 005
Revises: 004
Create Date: 2026-06-12 12:04:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('lich_hen',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('can_bo_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('tieu_de', sa.String(length=255), nullable=False),
        sa.Column('ngay_hen', sa.Date(), nullable=False),
        sa.Column('gio_hen', sa.Time(), nullable=False),
        sa.Column('ghi_chu', sa.Text(), nullable=True),
        sa.Column('trang_thai', sa.Enum('CHO_XAC_NHAN', 'DA_XAC_NHAN', 'DA_HUY', 'HOAN_THANH', name='trangthailichhenenum'), server_default='CHO_XAC_NHAN', nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['can_bo_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('lich_hen')
    op.execute('DROP TYPE trangthailichhenenum;')
