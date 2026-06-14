"""HoSo API router: CRUD + workflow + document upload."""
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.database.connection import get_db
from src.models.user import User, RoleEnum
from src.services import ho_so_service
from src.utils.response import success_response, error_response, build_pagination

router = APIRouter(prefix="/api/ho-so", tags=["Hồ sơ"])


# ─── Schemas ────────────────────────────────────────────────

class CreateHoSoInput(BaseModel):
    loai_thu_tuc: str
    noi_dung: str


class UpdateHoSoInput(BaseModel):
    noi_dung: str


class PheDuyetInput(BaseModel):
    ghi_chu: str = ""


class TuChoiInput(BaseModel):
    ly_do: str


class YeuCauBoSungInput(BaseModel):
    yeu_cau: str


# ─── CRUD Endpoints ─────────────────────────────────────────


@router.post("", status_code=201)
async def create_ho_so(
    data: CreateHoSoInput,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new ho so (citizen only)."""
    ho_so = await ho_so_service.create_ho_so(
        db=db, user_id=str(current_user.id),
        loai_thu_tuc=data.loai_thu_tuc, noi_dung=data.noi_dung,
    )
    return success_response({
        "id": str(ho_so.id),
        "ma_ho_so": ho_so.ma_ho_so,
        "loai_thu_tuc": ho_so.loai_thu_tuc,
        "trang_thai": ho_so.trang_thai.value,
        "ngay_nop": ho_so.ngay_nop.isoformat(),
    })


@router.get("")
async def list_ho_so(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    trang_thai: str | None = None,
    loai_thu_tuc: str | None = None,
    sort_by: str = "ngay_nop",
    sort_order: str = "desc",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List ho so with pagination and filters."""
    result = await ho_so_service.list_ho_so(
        db=db, current_user_id=str(current_user.id),
        role=current_user.role.value,
        page=page, limit=limit,
        trang_thai=trang_thai, loai_thu_tuc=loai_thu_tuc,
        sort_by=sort_by, sort_order=sort_order,
    )
    return success_response(
        data=[
            {
                "id": str(h.id),
                "ma_ho_so": h.ma_ho_so,
                "loai_thu_tuc": h.loai_thu_tuc,
                "trang_thai": h.trang_thai.value,
                "ngay_nop": h.ngay_nop.isoformat(),
            }
            for h in result["items"]
        ],
        pagination=result["pagination"],
    )


@router.get("/{ho_so_id}")
async def get_ho_so(
    ho_so_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get ho so detail."""
    ho_so = await ho_so_service.get_ho_so(
        db=db, ho_so_id=ho_so_id,
        current_user_id=str(current_user.id),
        role=current_user.role.value,
    )
    # Get documents
    tai_lieu_list = [
        {"id": str(tl.id), "ten_file": tl.ten_file, "loai_file": tl.loai_file}
        for tl in ho_so.tai_lieu
    ] if hasattr(ho_so, "tai_lieu") and ho_so.tai_lieu else []

    return success_response({
        "id": str(ho_so.id),
        "ma_ho_so": ho_so.ma_ho_so,
        "loai_thu_tuc": ho_so.loai_thu_tuc,
        "noi_dung": ho_so.noi_dung,
        "trang_thai": ho_so.trang_thai.value,
        "nguoi_nop": {"id": str(ho_so.user_id)},
        "nguoi_xu_ly": {"id": str(ho_so.nguoi_xu_ly_id)} if ho_so.nguoi_xu_ly_id else None,
        "tai_lieu": tai_lieu_list,
    })


@router.put("/{ho_so_id}")
async def update_ho_so(
    ho_so_id: str,
    data: UpdateHoSoInput,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update ho so content (only CHO_TIEP_NHAN)."""
    ho_so = await ho_so_service.update_ho_so(
        db=db, ho_so_id=ho_so_id,
        user_id=str(current_user.id), noi_dung=data.noi_dung,
    )
    return success_response({"message": "Cập nhật thành công"})


@router.delete("/{ho_so_id}")
async def delete_ho_so(
    ho_so_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete ho so (only CHO_TIEP_NHAN)."""
    await ho_so_service.delete_ho_so(
        db=db, ho_so_id=ho_so_id, user_id=str(current_user.id),
    )
    return success_response({"message": "Xoá hồ sơ thành công"})


# ─── Document Upload ────────────────────────────────────────


@router.post("/{ho_so_id}/upload")
async def upload_tai_lieu(
    ho_so_id: str,
    ten_file: str,
    loai_file: str,
    kich_thuoc: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload a document for a ho so."""
    duong_dan = f"uploads/{current_user.id}/{ho_so_id}/{ten_file}"
    tai_lieu = await ho_so_service.upload_tai_lieu(
        db=db, ho_so_id=ho_so_id, user_id=str(current_user.id),
        ten_file=ten_file, duong_dan=duong_dan,
        loai_file=loai_file, kich_thuoc=kich_thuoc,
    )
    return success_response({
        "id": str(tai_lieu.id),
        "ten_file": tai_lieu.ten_file,
        "loai_file": tai_lieu.loai_file,
        "kich_thuoc": tai_lieu.kich_thuoc,
        "duong_dan": tai_lieu.duong_dan,
    })


# ─── Workflow / State Machine ───────────────────────────────


@router.post("/{ho_so_id}/submit")
async def submit_ho_so(
    ho_so_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit ho so: CHO_TIEP_NHAN → CHO_XU_LY."""
    ho_so = await ho_so_service.submit_ho_so(
        db=db, ho_so_id=ho_so_id, user_id=str(current_user.id),
    )
    return success_response({
        "id": str(ho_so.id),
        "trang_thai": ho_so.trang_thai.value,
        "message": "Hồ sơ đã được nộp, chờ cán bộ tiếp nhận",
    })


@router.put("/{ho_so_id}/tiep-nhan")
async def tiep_nhan_ho_so(
    ho_so_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Receive ho so: CHO_XU_LY → DANG_XU_LY (officer only)."""
    if current_user.role == RoleEnum.citizen:
        from src.middleware.error_handler import ForbiddenException
        raise ForbiddenException("Chỉ cán bộ mới có thể tiếp nhận hồ sơ")

    ho_so = await ho_so_service.tiep_nhan_ho_so(
        db=db, ho_so_id=ho_so_id, can_bo_id=str(current_user.id),
    )
    return success_response({
        "id": str(ho_so.id),
        "trang_thai": ho_so.trang_thai.value,
        "nguoi_xu_ly": {"id": str(current_user.id), "ho_ten": current_user.ho_ten},
    })


@router.put("/{ho_so_id}/phe-duyet")
async def phe_duyet_ho_so(
    ho_so_id: str,
    data: PheDuyetInput,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Approve ho so: DANG_XU_LY → DA_XU_LY (officer only)."""
    if current_user.role == RoleEnum.citizen:
        from src.middleware.error_handler import ForbiddenException
        raise ForbiddenException("Chỉ cán bộ mới có thể phê duyệt hồ sơ")

    ho_so = await ho_so_service.phe_duyet_ho_so(
        db=db, ho_so_id=ho_so_id,
        can_bo_id=str(current_user.id), ghi_chu=data.ghi_chu,
    )
    return success_response({
        "id": str(ho_so.id),
        "trang_thai": ho_so.trang_thai.value,
        "message": "Hồ sơ đã được phê duyệt",
    })


@router.put("/{ho_so_id}/tu-choi")
async def tu_choi_ho_so(
    ho_so_id: str,
    data: TuChoiInput,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Reject ho so: DANG_XU_LY → TU_CHOI (officer only)."""
    if current_user.role == RoleEnum.citizen:
        from src.middleware.error_handler import ForbiddenException
        raise ForbiddenException("Chỉ cán bộ mới có thể từ chối hồ sơ")

    ho_so = await ho_so_service.tu_choi_ho_so(
        db=db, ho_so_id=ho_so_id,
        can_bo_id=str(current_user.id), ly_do=data.ly_do,
    )
    return success_response({
        "id": str(ho_so.id),
        "trang_thai": ho_so.trang_thai.value,
        "message": "Hồ sơ đã bị từ chối",
    })


@router.put("/{ho_so_id}/yeu-cau-bo-sung")
async def yeu_cau_bo_sung_ho_so(
    ho_so_id: str,
    data: YeuCauBoSungInput,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Request supplemental docs: DANG_XU_LY → CHO_BO_SUNG (officer only)."""
    if current_user.role == RoleEnum.citizen:
        from src.middleware.error_handler import ForbiddenException
        raise ForbiddenException("Chỉ cán bộ mới có thể yêu cầu bổ sung")

    ho_so = await ho_so_service.yeu_cau_bo_sung_ho_so(
        db=db, ho_so_id=ho_so_id,
        can_bo_id=str(current_user.id), yeu_cau=data.yeu_cau,
    )
    return success_response({
        "id": str(ho_so.id),
        "trang_thai": ho_so.trang_thai.value,
        "message": "Đã gửi yêu cầu bổ sung",
    })


@router.post("/{ho_so_id}/bo-sung")
async def bo_sung_ho_so(
    ho_so_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Citizen submits supplemental: CHO_BO_SUNG → DA_BO_SUNG."""
    ho_so = await ho_so_service.bo_sung_ho_so(
        db=db, ho_so_id=ho_so_id, user_id=str(current_user.id),
    )
    return success_response({
        "id": str(ho_so.id),
        "trang_thai": ho_so.trang_thai.value,
        "message": "Đã gửi bổ sung hồ sơ",
    })


@router.get("/{ho_so_id}/lich-su")
async def get_lich_su(
    ho_so_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get audit trail for a ho so."""
    lich_su_list = await ho_so_service.get_lich_su(
        db=db, ho_so_id=ho_so_id,
        user_id=str(current_user.id), role=current_user.role.value,
    )
    return success_response([
        {
            "id": str(ls.id),
            "hanh_dong": ls.hanh_dong,
            "trang_thai_cu": ls.trang_thai_cu,
            "trang_thai_moi": ls.trang_thai_moi,
            "ghi_chu": ls.ghi_chu,
            "created_at": ls.created_at.isoformat(),
        }
        for ls in lich_su_list
    ])
