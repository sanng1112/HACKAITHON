"""ThongBao API router: notifications CRUD."""
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.database.connection import get_db
from src.models.user import User, RoleEnum
from src.services import thong_bao_service
from src.utils.response import success_response

router = APIRouter(prefix="/api/thong-bao", tags=["Thông báo"])


# ─── Schemas ────────────────────────────────────────────────

class CreateThongBaoInput(BaseModel):
    user_id: str | None = None  # null = broadcast
    tieu_de: str
    noi_dung: str
    loai: str  # he_thong | ho_so | lich_hen


# ─── Endpoints ──────────────────────────────────────────────


@router.post("", status_code=201)
async def create_thong_bao(
    data: CreateThongBaoInput,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a notification (officer/admin only)."""
    if current_user.role == RoleEnum.citizen:
        from src.middleware.error_handler import ForbiddenException
        raise ForbiddenException("Chỉ cán bộ mới có thể tạo thông báo")

    thong_bao = await thong_bao_service.create_notification(
        db=db, user_id=data.user_id,
        tieu_de=data.tieu_de, noi_dung=data.noi_dung, loai=data.loai,
    )
    return success_response({"id": str(thong_bao.id), "message": "Thông báo đã được gửi"})


@router.get("")
async def list_thong_bao(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    da_doc: bool | None = None,
    loai: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List notifications for current user."""
    result = await thong_bao_service.list_notifications(
        db=db, user_id=str(current_user.id),
        page=page, limit=limit, da_doc=da_doc, loai=loai,
    )
    return success_response(
        data=[
            {
                "id": str(tb.id),
                "tieu_de": tb.tieu_de,
                "noi_dung": tb.noi_dung,
                "loai": tb.loai.value,
                "da_doc": tb.da_doc,
                "created_at": tb.created_at.isoformat(),
            }
            for tb in result["items"]
        ],
        pagination=result["pagination"],
    )


@router.put("/{thong_bao_id}/da-doc")
async def mark_as_read(
    thong_bao_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a notification as read."""
    await thong_bao_service.mark_as_read(
        db=db, thong_bao_id=thong_bao_id, user_id=str(current_user.id),
    )
    return success_response({"message": "Đã đánh dấu đã đọc"})
