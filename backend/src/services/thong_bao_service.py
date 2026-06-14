"""ThongBao (notification) service — CRUD + auto-notifications."""
import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repositories.thong_bao_repository import thong_bao_repo
from src.middleware.error_handler import BusinessRuleException, NotFoundException
from src.models.thong_bao import LoaiThongBaoEnum, ThongBao
from src.utils.response import build_pagination


async def create_notification(
    db: AsyncSession,
    user_id: Optional[str],
    tieu_de: str,
    noi_dung: str,
    loai: str,
) -> ThongBao:
    """
    Create a notification.

    If user_id is None, it's a broadcast sent to all users.
    """
    try:
        loai_enum = LoaiThongBaoEnum(loai)
    except ValueError:
        raise BusinessRuleException(f"Loại thông báo '{loai}' không hợp lệ")

    thong_bao = await thong_bao_repo.create(
        db,
        obj_in={
            "id": uuid.uuid4(),
            "user_id": user_id if user_id else None,
            "tieu_de": tieu_de,
            "noi_dung": noi_dung,
            "loai": loai_enum,
            "da_doc": False,
        },
    )
    return thong_bao


async def list_notifications(
    db: AsyncSession,
    user_id: str,
    page: int = 1,
    limit: int = 20,
    da_doc: Optional[bool] = None,
    loai: Optional[str] = None,
) -> dict:
    """List notifications for the current user (including broadcasts)."""
    skip = (page - 1) * limit

    loai_enum = None
    if loai:
        try:
            loai_enum = LoaiThongBaoEnum(loai)
        except ValueError:
            raise BusinessRuleException(f"Loại thông báo '{loai}' không hợp lệ")

    items, total = await thong_bao_repo.get_paginated_for_user(
        db,
        user_id=user_id,
        skip=skip,
        limit=limit,
        da_doc=da_doc,
        loai=loai_enum,
    )

    return {
        "items": items,
        "pagination": build_pagination(page, limit, total),
    }


async def mark_as_read(db: AsyncSession, thong_bao_id: str, user_id: str) -> ThongBao:
    """Mark a notification as read."""
    thong_bao = await thong_bao_repo.get(db, id=thong_bao_id)
    if not thong_bao:
        raise NotFoundException("Thông báo")

    # User can only mark their own (or broadcast) notifications
    if thong_bao.user_id is not None and str(thong_bao.user_id) != user_id:
        raise NotFoundException("Thông báo")

    return await thong_bao_repo.update(
        db, db_obj=thong_bao, obj_in={"da_doc": True}
    )
