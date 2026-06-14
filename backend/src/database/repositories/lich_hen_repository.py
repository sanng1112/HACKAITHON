from typing import Optional, Tuple
from datetime import date, time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from src.models.lich_hen import LichHen, TrangThaiLichHenEnum
from .base_repository import BaseRepository


class LichHenRepository(BaseRepository[LichHen]):
    def __init__(self):
        super().__init__(LichHen)

    async def check_conflict(self, db: AsyncSession, ngay_hen: date, gio_hen: time, exclude_id: Optional[str] = None) -> bool:
        """Check if a time slot is already booked."""
        query = select(LichHen).where(
            LichHen.ngay_hen == ngay_hen,
            LichHen.gio_hen == gio_hen,
            LichHen.trang_thai.in_([TrangThaiLichHenEnum.CHO_XAC_NHAN, TrangThaiLichHenEnum.DA_XAC_NHAN]),
        )
        if exclude_id:
            query = query.where(LichHen.id != exclude_id)
        result = await db.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_paginated_with_filters(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        trang_thai: Optional[TrangThaiLichHenEnum] = None,
        user_id: Optional[str] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> Tuple[list[LichHen], int]:
        """Return (items, total_count) with filters."""
        # Count query
        count_query = select(func.count(LichHen.id))
        if trang_thai:
            count_query = count_query.filter(LichHen.trang_thai == trang_thai)
        if user_id:
            count_query = count_query.filter(LichHen.user_id == user_id)
        if from_date:
            count_query = count_query.filter(LichHen.ngay_hen >= from_date)
        if to_date:
            count_query = count_query.filter(LichHen.ngay_hen <= to_date)
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        # Data query
        query = select(LichHen)
        if trang_thai:
            query = query.filter(LichHen.trang_thai == trang_thai)
        if user_id:
            query = query.filter(LichHen.user_id == user_id)
        if from_date:
            query = query.filter(LichHen.ngay_hen >= from_date)
        if to_date:
            query = query.filter(LichHen.ngay_hen <= to_date)
        query = query.order_by(LichHen.ngay_hen.asc(), LichHen.gio_hen.asc())
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all()), total


lich_hen_repo = LichHenRepository()
