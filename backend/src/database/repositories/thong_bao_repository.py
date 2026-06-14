from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from src.models.thong_bao import ThongBao, LoaiThongBaoEnum
from .base_repository import BaseRepository


class ThongBaoRepository(BaseRepository[ThongBao]):
    def __init__(self):
        super().__init__(ThongBao)

    async def get_paginated_for_user(
        self,
        db: AsyncSession,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        da_doc: Optional[bool] = None,
        loai: Optional[LoaiThongBaoEnum] = None,
    ) -> Tuple[list[ThongBao], int]:
        """Return notifications for user (personal + broadcast) with count."""
        # Count
        count_query = select(func.count(ThongBao.id)).where(
            or_(ThongBao.user_id == user_id, ThongBao.user_id.is_(None))
        )
        if da_doc is not None:
            count_query = count_query.filter(ThongBao.da_doc == da_doc)
        if loai:
            count_query = count_query.filter(ThongBao.loai == loai)
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        # Data
        query = select(ThongBao).where(
            or_(ThongBao.user_id == user_id, ThongBao.user_id.is_(None))
        )
        if da_doc is not None:
            query = query.filter(ThongBao.da_doc == da_doc)
        if loai:
            query = query.filter(ThongBao.loai == loai)
        query = query.order_by(ThongBao.created_at.desc())
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all()), total


thong_bao_repo = ThongBaoRepository()
