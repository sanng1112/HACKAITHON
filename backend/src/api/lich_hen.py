"""LichHen API router: CRUD appointments with conflict detection."""
from datetime import date
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.database.connection import get_db
from src.models.user import User
from src.services import lich_hen_service
from src.utils.response import success_response

router = APIRouter(prefix="/api/lich-hen", tags=["Lịch hẹn"])


# ─── Schemas ────────────────────────────────────────────────

class CreateLichHenInput(BaseModel):
    tieu_de: str
    ngay_hen: date
    gio_hen: str  # "HH:MM"
    ghi_chu: str | None = None


class UpdateLichHenInput(BaseModel):
    trang_thai: str | None = None
    can_bo_id: str | None = None
    ghi_chu: str | None = None


# ─── Endpoints ──────────────────────────────────────────────


@router.post("", status_code=201)
async def create_lich_hen(
    data: CreateLichHenInput,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new appointment."""
    from datetime import time
    gio, phut = map(int, data.gio_hen.split(":"))
    gio_hen = time(hour=gio, minute=phut)

    lich_hen = await lich_hen_service.create_lich_hen(
        db=db, user_id=str(current_user.id),
        tieu_de=data.tieu_de, ngay_hen=data.ngay_hen,
        gio_hen=gio_hen, ghi_chu=data.ghi_chu,
    )
    return success_response({
        "id": str(lich_hen.id),
        "tieu_de": lich_hen.tieu_de,
        "ngay_hen": lich_hen.ngay_hen.isoformat(),
        "gio_hen": lich_hen.gio_hen.strftime("%H:%M"),
        "trang_thai": lich_hen.trang_thai.value,
    })


@router.get("")
async def list_lich_hen(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    trang_thai: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List appointments with pagination."""
    result = await lich_hen_service.list_lich_hen(
        db=db, current_user_id=str(current_user.id),
        role=current_user.role.value,
        page=page, limit=limit,
        trang_thai=trang_thai,
        from_date=from_date, to_date=to_date,
    )
    return success_response(
        data=[
            {
                "id": str(lh.id),
                "tieu_de": lh.tieu_de,
                "ngay_hen": lh.ngay_hen.isoformat(),
                "gio_hen": lh.gio_hen.strftime("%H:%M"),
                "trang_thai": lh.trang_thai.value,
            }
            for lh in result["items"]
        ],
        pagination=result["pagination"],
    )


@router.get("/{lich_hen_id}")
async def get_lich_hen(
    lich_hen_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get appointment detail."""
    lich_hen = await lich_hen_service.get_lich_hen(
        db=db, lich_hen_id=lich_hen_id,
        current_user_id=str(current_user.id),
        role=current_user.role.value,
    )
    return success_response({
        "id": str(lich_hen.id),
        "tieu_de": lich_hen.tieu_de,
        "ngay_hen": lich_hen.ngay_hen.isoformat(),
        "gio_hen": lich_hen.gio_hen.strftime("%H:%M"),
        "trang_thai": lich_hen.trang_thai.value,
        "ghi_chu": lich_hen.ghi_chu,
    })


@router.put("/{lich_hen_id}")
async def update_lich_hen(
    lich_hen_id: str,
    data: UpdateLichHenInput,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update/cancel appointment."""
    lich_hen = await lich_hen_service.update_lich_hen(
        db=db, lich_hen_id=lich_hen_id,
        current_user_id=str(current_user.id),
        role=current_user.role.value,
        trang_thai=data.trang_thai,
        can_bo_id=data.can_bo_id,
        ghi_chu=data.ghi_chu,
    )
    return success_response({"message": "Cập nhật thành công"})


@router.delete("/{lich_hen_id}")
async def delete_lich_hen(
    lich_hen_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Cancel appointment (must be > 24h before)."""
    await lich_hen_service.delete_lich_hen(
        db=db, lich_hen_id=lich_hen_id, user_id=str(current_user.id),
    )
    return success_response({"message": "Đã huỷ lịch hẹn"})
