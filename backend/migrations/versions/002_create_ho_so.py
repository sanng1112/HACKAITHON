"""create ho so

Revision ID: 002
Revises: 001
Create Date: 2026-06-12 12:01:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('ho_so',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ma_ho_so', sa.String(length=30), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('loai_thu_tuc', sa.String(length=100), nullable=False),
        sa.Column('noi_dung', sa.Text(), nullable=False),
        sa.Column('trang_thai', sa.Enum('CHO_TIEP_NHAN', 'CHO_XU_LY', 'DANG_XU_LY', 'DA_XU_LY', 'TU_CHOI', 'CHO_BO_SUNG', 'DA_BO_SUNG', name='trangthaihosoenum'), server_default='CHO_TIEP_NHAN', nullable=False),
        sa.Column('nguoi_xu_ly_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('ghi_chu_xu_ly', sa.Text(), nullable=True),
        sa.Column('ly_do_tu_choi', sa.Text(), nullable=True),
        sa.Column('yeu_cau_bo_sung', sa.Text(), nullable=True),
        sa.Column('ngay_nop', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('ngay_xu_ly', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['nguoi_xu_ly_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ma_ho_so')
    )

def downgrade():
    op.drop_table('ho_so')
    op.execute('DROP TYPE trangthaihosoenum;')
