from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.ho_so_lich_su import HoSoLichSu
from .base_repository import BaseRepository

class HoSoLichSuRepository(BaseRepository[HoSoLichSu]):
    def __init__(self):
        super().__init__(HoSoLichSu)

    async def get_by_ho_so(self, db: AsyncSession, ho_so_id: str):
        result = await db.execute(select(HoSoLichSu).filter(HoSoLichSu.ho_so_id == ho_so_id).order_by(HoSoLichSu.created_at.desc()))
        return result.scalars().all()

ho_so_lich_su_repo = HoSoLichSuRepository()
