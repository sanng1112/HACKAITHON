from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.ho_so_tai_lieu import HoSoTaiLieu
from .base_repository import BaseRepository

class HoSoTaiLieuRepository(BaseRepository[HoSoTaiLieu]):
    def __init__(self):
        super().__init__(HoSoTaiLieu)

    async def get_by_ho_so(self, db: AsyncSession, ho_so_id: str):
        result = await db.execute(select(HoSoTaiLieu).filter(HoSoTaiLieu.ho_so_id == ho_so_id))
        return result.scalars().all()

ho_so_tai_lieu_repo = HoSoTaiLieuRepository()
