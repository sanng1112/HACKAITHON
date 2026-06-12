import uuid
import enum
from sqlalchemy import Column, String, Text, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from src.database.base import Base

class RoleEnum(str, enum.Enum):
    citizen = 'citizen'
    officer = 'officer'
    admin = 'admin'

class StatusEnum(str, enum.Enum):
    active = 'active'
    inactive = 'inactive'
    locked = 'locked'

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    ho_ten = Column(String(255), nullable=False)
    so_cccd = Column(String(20), unique=True, index=True)
    so_dien_thoai = Column(String(20))
    dia_chi = Column(Text)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.citizen, index=True)
    trang_thai = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.active)
    refresh_token = Column(Text)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
