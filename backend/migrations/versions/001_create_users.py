"""create users

Revision ID: 001
Revises: 
Create Date: 2026-06-12 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('ho_ten', sa.String(length=255), nullable=False),
        sa.Column('so_cccd', sa.String(length=20), nullable=True),
        sa.Column('so_dien_thoai', sa.String(length=20), nullable=True),
        sa.Column('dia_chi', sa.Text(), nullable=True),
        sa.Column('role', sa.Enum('citizen', 'officer', 'admin', name='roleenum'), server_default='citizen', nullable=False),
        sa.Column('trang_thai', sa.Enum('active', 'inactive', 'locked', name='statusenum'), server_default='active', nullable=False),
        sa.Column('refresh_token', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('so_cccd')
    )

def downgrade():
    op.drop_table('users')
    op.execute('DROP TYPE roleenum;')
    op.execute('DROP TYPE statusenum;')
