import uuid
from sqlalchemy import Column, String, Text, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.database.base import Base

class HoSoLichSu(Base):
    __tablename__ = 'ho_so_lich_su'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ho_so_id = Column(UUID(as_uuid=True), ForeignKey('ho_so.id'), nullable=False, index=True)
    nguoi_thuc_hien_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    hanh_dong = Column(String(50), nullable=False)
    trang_thai_cu = Column(String(30))
    trang_thai_moi = Column(String(30))
    ghi_chu = Column(Text)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
