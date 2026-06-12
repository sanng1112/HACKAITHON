"""create thong bao

Revision ID: 006
Revises: 005
Create Date: 2026-06-12 12:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('thong_bao',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('tieu_de', sa.String(length=255), nullable=False),
        sa.Column('noi_dung', sa.Text(), nullable=False),
        sa.Column('loai', sa.Enum('he_thong', 'ho_so', 'lich_hen', name='loaithongbaoenum'), nullable=False),
        sa.Column('da_doc', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('thong_bao')
    op.execute('DROP TYPE loaithongbaoenum;')
