import uuid
import enum
from sqlalchemy import Column, String, Text, Enum, DateTime, Date, Time, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.database.base import Base

class TrangThaiLichHenEnum(str, enum.Enum):
    CHO_XAC_NHAN = 'CHO_XAC_NHAN'
    DA_XAC_NHAN = 'DA_XAC_NHAN'
    DA_HUY = 'DA_HUY'
    HOAN_THANH = 'HOAN_THANH'

class LichHen(Base):
    __tablename__ = 'lich_hen'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    can_bo_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    tieu_de = Column(String(255), nullable=False)
    ngay_hen = Column(Date, nullable=False, index=True)
    gio_hen = Column(Time, nullable=False)
    ghi_chu = Column(Text)
    trang_thai = Column(Enum(TrangThaiLichHenEnum), default=TrangThaiLichHenEnum.CHO_XAC_NHAN, index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
