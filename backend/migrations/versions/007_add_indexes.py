"""add indexes

Revision ID: 007
Revises: 006
Create Date: 2026-06-12 12:06:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None

def upgrade():
    # users
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_so_cccd'), 'users', ['so_cccd'], unique=True)
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)
    
    # ho_so
    op.create_index(op.f('ix_ho_so_ma_ho_so'), 'ho_so', ['ma_ho_so'], unique=True)
    op.create_index(op.f('ix_ho_so_user_id'), 'ho_so', ['user_id'], unique=False)
    op.create_index(op.f('ix_ho_so_trang_thai'), 'ho_so', ['trang_thai'], unique=False)
    op.create_index(op.f('ix_ho_so_ngay_nop'), 'ho_so', ['ngay_nop'], unique=False)
    
    # ho_so_lich_su
    op.create_index(op.f('ix_ho_so_lich_su_ho_so_id'), 'ho_so_lich_su', ['ho_so_id'], unique=False)
    op.create_index(op.f('ix_ho_so_lich_su_created_at'), 'ho_so_lich_su', ['created_at'], unique=False)
    
    # lich_hen
    op.create_index(op.f('ix_lich_hen_user_id'), 'lich_hen', ['user_id'], unique=False)
    op.create_index(op.f('ix_lich_hen_ngay_hen'), 'lich_hen', ['ngay_hen'], unique=False)
    op.create_index(op.f('ix_lich_hen_trang_thai'), 'lich_hen', ['trang_thai'], unique=False)
    
    # thong_bao
    op.create_index(op.f('ix_thong_bao_user_id'), 'thong_bao', ['user_id'], unique=False)
    op.create_index(op.f('ix_thong_bao_da_doc'), 'thong_bao', ['da_doc'], unique=False)
    op.create_index(op.f('ix_thong_bao_created_at'), 'thong_bao', ['created_at'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_thong_bao_created_at'), table_name='thong_bao')
    op.drop_index(op.f('ix_thong_bao_da_doc'), table_name='thong_bao')
    op.drop_index(op.f('ix_thong_bao_user_id'), table_name='thong_bao')
    
    op.drop_index(op.f('ix_lich_hen_trang_thai'), table_name='lich_hen')
    op.drop_index(op.f('ix_lich_hen_ngay_hen'), table_name='lich_hen')
    op.drop_index(op.f('ix_lich_hen_user_id'), table_name='lich_hen')
    
    op.drop_index(op.f('ix_ho_so_lich_su_created_at'), table_name='ho_so_lich_su')
    op.drop_index(op.f('ix_ho_so_lich_su_ho_so_id'), table_name='ho_so_lich_su')
    
    op.drop_index(op.f('ix_ho_so_ngay_nop'), table_name='ho_so')
    op.drop_index(op.f('ix_ho_so_trang_thai'), table_name='ho_so')
    op.drop_index(op.f('ix_ho_so_user_id'), table_name='ho_so')
    op.drop_index(op.f('ix_ho_so_ma_ho_so'), table_name='ho_so')
    
    op.drop_index(op.f('ix_users_role'), table_name='users')
    op.drop_index(op.f('ix_users_so_cccd'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
