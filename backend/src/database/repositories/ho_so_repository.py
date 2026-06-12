from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.models.ho_so import HoSo, TrangThaiHoSoEnum
from .base_repository import BaseRepository

class HoSoRepository(BaseRepository[HoSo]):
    def __init__(self):
        super().__init__(HoSo)

    async def get_paginated_with_filters(
        self, db: AsyncSession, skip: int = 0, limit: int = 100,
        trang_thai: Optional[TrangThaiHoSoEnum] = None,
        user_id: Optional[str] = None
    ):
        query = select(HoSo)
        if trang_thai:
            query = query.filter(HoSo.trang_thai == trang_thai)
        if user_id:
            query = query.filter(HoSo.user_id == user_id)
            
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

ho_so_repo = HoSoRepository()
