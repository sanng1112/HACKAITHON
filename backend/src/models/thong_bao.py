import uuid
import enum
from sqlalchemy import Column, String, Text, Enum, DateTime, Boolean, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.database.base import Base

class LoaiThongBaoEnum(str, enum.Enum):
    he_thong = 'he_thong'
    ho_so = 'ho_so'
    lich_hen = 'lich_hen'

class ThongBao(Base):
    __tablename__ = 'thong_bao'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    tieu_de = Column(String(255), nullable=False)
    noi_dung = Column(Text, nullable=False)
    loai = Column(Enum(LoaiThongBaoEnum), nullable=False)
    da_doc = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
