import uuid
import enum
from sqlalchemy import Column, String, Text, Enum, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.base import Base

class TrangThaiHoSoEnum(str, enum.Enum):
    CHO_TIEP_NHAN = 'CHO_TIEP_NHAN'
    CHO_XU_LY = 'CHO_XU_LY'
    DANG_XU_LY = 'DANG_XU_LY'
    DA_XU_LY = 'DA_XU_LY'
    TU_CHOI = 'TU_CHOI'
    CHO_BO_SUNG = 'CHO_BO_SUNG'
    DA_BO_SUNG = 'DA_BO_SUNG'

class HoSo(Base):
    __tablename__ = 'ho_so'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ma_ho_so = Column(String(30), unique=True, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    loai_thu_tuc = Column(String(100), nullable=False)
    noi_dung = Column(Text, nullable=False)
    trang_thai = Column(Enum(TrangThaiHoSoEnum), nullable=False, default=TrangThaiHoSoEnum.CHO_TIEP_NHAN, index=True)
    nguoi_xu_ly_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    ghi_chu_xu_ly = Column(Text)
    ly_do_tu_choi = Column(Text)
    yeu_cau_bo_sung = Column(Text)
    ngay_nop = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    ngay_xu_ly = Column(DateTime)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship("User", foreign_keys=[user_id])
    nguoi_xu_ly = relationship("User", foreign_keys=[nguoi_xu_ly_id])
