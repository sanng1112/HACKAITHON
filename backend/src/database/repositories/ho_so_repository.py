from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from src.models.ho_so import HoSo, TrangThaiHoSoEnum
from .base_repository import BaseRepository


class HoSoRepository(BaseRepository[HoSo]):
    def __init__(self):
        super().__init__(HoSo)

    async def get_paginated_with_filters(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        trang_thai: Optional[TrangThaiHoSoEnum] = None,
        user_id: Optional[str] = None,
        loai_thu_tuc: Optional[str] = None,
        sort_by: str = "ngay_nop",
        sort_order: str = "desc",
    ):
        query = select(HoSo)
        if trang_thai:
            query = query.filter(HoSo.trang_thai == trang_thai)
        if user_id:
            query = query.filter(HoSo.user_id == user_id)
        if loai_thu_tuc:
            query = query.filter(HoSo.loai_thu_tuc == loai_thu_tuc)

        # Apply sorting
        sort_column = getattr(HoSo, sort_by, HoSo.ngay_nop)
        if sort_order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def count_with_filters(
        self,
        db: AsyncSession,
        trang_thai: Optional[TrangThaiHoSoEnum] = None,
        user_id: Optional[str] = None,
        loai_thu_tuc: Optional[str] = None,
    ) -> int:
        query = select(func.count(HoSo.id))
        if trang_thai:
            query = query.filter(HoSo.trang_thai == trang_thai)
        if user_id:
            query = query.filter(HoSo.user_id == user_id)
        if loai_thu_tuc:
            query = query.filter(HoSo.loai_thu_tuc == loai_thu_tuc)

        result = await db.execute(query)
        return result.scalar() or 0


ho_so_repo = HoSoRepository()
