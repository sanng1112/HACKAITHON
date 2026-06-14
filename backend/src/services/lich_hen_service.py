"""LichHen (appointment) service — CRUD + conflict detection."""
import uuid
from datetime import date, datetime, time, timedelta, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repositories.lich_hen_repository import lich_hen_repo
from src.middleware.error_handler import (
    BusinessRuleException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
)
from src.models.lich_hen import LichHen, TrangThaiLichHenEnum
from src.models.user import RoleEnum
from src.utils.response import build_pagination


async def create_lich_hen(
    db: AsyncSession,
    user_id: str,
    tieu_de: str,
    ngay_hen: date,
    gio_hen: time,
    ghi_chu: Optional[str] = None,
) -> LichHen:
    """Create a new appointment with conflict detection."""
    # Verify no conflict at the same time
    conflict = await lich_hen_repo.check_conflict(db, ngay_hen, gio_hen)
    if conflict:
        raise ConflictException(
            code="SCHEDULE_CONFLICT",
            message="Khung giờ này đã có lịch hẹn khác",
        )

    lich_hen = await lich_hen_repo.create(
        db,
        obj_in={
            "id": uuid.uuid4(),
            "user_id": user_id,
            "tieu_de": tieu_de,
            "ngay_hen": ngay_hen,
            "gio_hen": gio_hen,
            "ghi_chu": ghi_chu,
            "trang_thai": TrangThaiLichHenEnum.CHO_XAC_NHAN,
        },
    )
    return lich_hen


async def get_lich_hen(
    db: AsyncSession, lich_hen_id: str, current_user_id: str, role: str
) -> LichHen:
    """Get appointment detail. Citizen only sees own; officer/admin see all."""
    lich_hen = await lich_hen_repo.get(db, id=lich_hen_id)
    if not lich_hen:
        raise NotFoundException("Lịch hẹn")

    if role == RoleEnum.citizen.value and str(lich_hen.user_id) != current_user_id:
        raise ForbiddenException("Bạn không có quyền xem lịch hẹn này")

    return lich_hen


async def list_lich_hen(
    db: AsyncSession,
    current_user_id: str,
    role: str,
    page: int = 1,
    limit: int = 20,
    trang_thai: Optional[str] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> dict:
    """List appointments with pagination and filters."""
    skip = (page - 1) * limit

    if role == RoleEnum.citizen.value:
        user_id = current_user_id
    else:
        user_id = None

    trang_thai_enum = None
    if trang_thai:
        try:
            trang_thai_enum = TrangThaiLichHenEnum(trang_thai)
        except ValueError:
            raise BusinessRuleException(f"Trạng thái '{trang_thai}' không hợp lệ")

    items, total = await lich_hen_repo.get_paginated_with_filters(
        db,
        skip=skip,
        limit=limit,
        trang_thai=trang_thai_enum,
        user_id=user_id,
        from_date=from_date,
        to_date=to_date,
    )

    return {
        "items": items,
        "pagination": build_pagination(page, limit, total),
    }


async def update_lich_hen(
    db: AsyncSession,
    lich_hen_id: str,
    current_user_id: str,
    role: str,
    trang_thai: Optional[str] = None,
    can_bo_id: Optional[str] = None,
    ghi_chu: Optional[str] = None,
) -> LichHen:
    """Update appointment (confirm, reschedule, etc.)."""
    lich_hen = await lich_hen_repo.get(db, id=lich_hen_id)
    if not lich_hen:
        raise NotFoundException("Lịch hẹn")

    if role == RoleEnum.citizen.value and str(lich_hen.user_id) != current_user_id:
        raise ForbiddenException("Bạn không có quyền cập nhật lịch hẹn này")

    update_data: dict = {}
    if trang_thai:
        try:
            new_trang_thai = TrangThaiLichHenEnum(trang_thai)
        except ValueError:
            raise BusinessRuleException(f"Trạng thái '{trang_thai}' không hợp lệ")
        update_data["trang_thai"] = new_trang_thai

    if can_bo_id:
        update_data["can_bo_id"] = can_bo_id
    if ghi_chu:
        update_data["ghi_chu"] = ghi_chu

    return await lich_hen_repo.update(db, db_obj=lich_hen, obj_in=update_data)


async def delete_lich_hen(
    db: AsyncSession, lich_hen_id: str, user_id: str
) -> None:
    """Cancel appointment. Only allowed if >= 24h before the appointment."""
    lich_hen = await lich_hen_repo.get(db, id=lich_hen_id)
    if not lich_hen:
        raise NotFoundException("Lịch hẹn")

    if str(lich_hen.user_id) != user_id:
        raise ForbiddenException("Bạn không có quyền huỷ lịch hẹn này")

    # Check 24h rule
    appointment_dt = datetime.combine(lich_hen.ngay_hen, lich_hen.gio_hen).replace(
        tzinfo=timezone.utc
    )
    now = datetime.now(timezone.utc)
    if appointment_dt - now < timedelta(hours=24):
        raise BusinessRuleException("Chỉ được huỷ lịch hẹn trước 24 giờ")

    await lich_hen_repo.update(
        db, db_obj=lich_hen, obj_in={"trang_thai": TrangThaiLichHenEnum.DA_HUY}
    )
