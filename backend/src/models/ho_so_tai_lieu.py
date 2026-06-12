import uuid
from sqlalchemy import Column, String, Text, DateTime, func, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from src.database.base import Base

class HoSoTaiLieu(Base):
    __tablename__ = 'ho_so_tai_lieu'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ho_so_id = Column(UUID(as_uuid=True), ForeignKey('ho_so.id'), nullable=False)
    ten_file = Column(String(255), nullable=False)
    duong_dan = Column(Text, nullable=False)
    loai_file = Column(String(50), nullable=False)
    kich_thuoc = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
