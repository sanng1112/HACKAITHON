"""HoSo (administrative dossier) service — CRUD + state machine workflow."""
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repositories.ho_so_repository import ho_so_repo
from src.database.repositories.ho_so_lich_su_repository import ho_so_lich_su_repo
from src.database.repositories.ho_so_tai_lieu_repository import ho_so_tai_lieu_repo
from src.middleware.error_handler import (
    BusinessRuleException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
)
from src.models.ho_so import HoSo, TrangThaiHoSoEnum
from src.models.ho_so_lich_su import HoSoLichSu
from src.models.ho_so_tai_lieu import HoSoTaiLieu
from src.models.user import RoleEnum
from src.services.thong_bao_service import create_notification
from src.utils.response import build_pagination

# ---- State Machine Configuration ----

TRANSITIONS: dict[TrangThaiHoSoEnum, dict[str, TrangThaiHoSoEnum]] = {
    TrangThaiHoSoEnum.CHO_TIEP_NHAN: {"submit": TrangThaiHoSoEnum.CHO_XU_LY},
    TrangThaiHoSoEnum.CHO_XU_LY: {"tiep_nhan": TrangThaiHoSoEnum.DANG_XU_LY},
    TrangThaiHoSoEnum.DANG_XU_LY: {
        "phe_duyet": TrangThaiHoSoEnum.DA_XU_LY,
        "tu_choi": TrangThaiHoSoEnum.TU_CHOI,
        "yeu_cau_bo_sung": TrangThaiHoSoEnum.CHO_BO_SUNG,
    },
    TrangThaiHoSoEnum.CHO_BO_SUNG: {"bo_sung": TrangThaiHoSoEnum.DA_BO_SUNG},
    TrangThaiHoSoEnum.DA_BO_SUNG: {"nhan_bo_sung": TrangThaiHoSoEnum.DANG_XU_LY},
}

TRANG_THAI_LABEL = {
    TrangThaiHoSoEnum.CHO_TIEP_NHAN: "Chờ tiếp nhận",
    TrangThaiHoSoEnum.CHO_XU_LY: "Chờ xử lý",
    TrangThaiHoSoEnum.DANG_XU_LY: "Đang xử lý",
    TrangThaiHoSoEnum.DA_XU_LY: "Đã xử lý",
    TrangThaiHoSoEnum.TU_CHOI: "Từ chối",
    TrangThaiHoSoEnum.CHO_BO_SUNG: "Chờ bổ sung",
    TrangThaiHoSoEnum.DA_BO_SUNG: "Đã bổ sung",
}

# ─── Helpers ─────────────────────────────────────────────────


def _validate_transition(ho_so: HoSo, action: str) -> TrangThaiHoSoEnum:
    """Validate and return the next state for an action."""
    current = ho_so.trang_thai
    if current not in TRANSITIONS or action not in TRANSITIONS[current]:
        raise BusinessRuleException(
            f"Không thể thực hiện '{action}' khi hồ sơ ở trạng thái '{TRANG_THAI_LABEL[current]}'"
        )
    return TRANSITIONS[current][action]


async def _ghi_lich_su(
    db: AsyncSession,
    ho_so_id: str,
    hanh_dong: str,
    trang_thai_cu: Optional[str],
    trang_thai_moi: Optional[str],
    nguoi_thuc_hien_id: str,
    ghi_chu: str = "",
) -> HoSoLichSu:
    """Record an audit trail entry for the ho so."""
    return await ho_so_lich_su_repo.create(
        db,
        obj_in={
            "id": uuid.uuid4(),
            "ho_so_id": ho_so_id,
            "nguoi_thuc_hien_id": nguoi_thuc_hien_id,
            "hanh_dong": hanh_dong,
            "trang_thai_cu": trang_thai_cu,
            "trang_thai_moi": trang_thai_moi,
            "ghi_chu": ghi_chu or None,
        },
    )


async def _notify_status_change(db: AsyncSession, ho_so: HoSo) -> None:
    """Send auto-notification when ho so status changes."""
    label = TRANG_THAI_LABEL.get(ho_so.trang_thai, ho_so.trang_thai.value)
    await create_notification(
        db,
        user_id=str(ho_so.user_id),
        tieu_de=f"Hồ sơ {ho_so.ma_ho_so} đã chuyển sang '{label}'",
        noi_dung=f"Hồ sơ {ho_so.ma_ho_so} của bạn đã được cập nhật. Trạng thái hiện tại: {label}.",
        loai="ho_so",
    )


async def _sinh_ma_ho_so(db: AsyncSession) -> str:
    """Generate unique ho so code: HS-{YYYY}-{XXXX}."""
    from sqlalchemy import func, select
    from src.models.ho_so import HoSo

    year = datetime.now(timezone.utc).year
    query = select(func.count(HoSo.id)).where(
        func.extract("year", HoSo.ngay_nop) == year
    )
    result = await db.execute(query)
    count = result.scalar() or 0
    next_num = count + 1
    return f"HS-{year}-{next_num:04d}"


# ─── CRUD Operations ─────────────────────────────────────────


async def create_ho_so(
    db: AsyncSession, user_id: str, loai_thu_tuc: str, noi_dung: str
) -> HoSo:
    """Create a new ho so in CHO_TIEP_NHAN state."""
    ma_ho_so = await _sinh_ma_ho_so(db)
    ho_so = await ho_so_repo.create(
        db,
        obj_in={
            "id": uuid.uuid4(),
            "ma_ho_so": ma_ho_so,
            "user_id": user_id,
            "loai_thu_tuc": loai_thu_tuc,
            "noi_dung": noi_dung,
            "trang_thai": TrangThaiHoSoEnum.CHO_TIEP_NHAN,
        },
    )

    await _ghi_lich_su(
        db, str(ho_so.id), "TAO_MOI", None, TrangThaiHoSoEnum.CHO_TIEP_NHAN.value, user_id
    )
    return ho_so


async def get_ho_so(db: AsyncSession, ho_so_id: str, current_user_id: str, role: str) -> HoSo:
    """Get ho so detail. Citizen can only see own; officer/admin see all."""
    ho_so = await ho_so_repo.get(db, id=ho_so_id)
    if not ho_so:
        raise NotFoundException("Hồ sơ")

    if role == RoleEnum.citizen.value and str(ho_so.user_id) != current_user_id:
        raise ForbiddenException("Bạn không có quyền xem hồ sơ này")

    return ho_so


async def list_ho_so(
    db: AsyncSession,
    current_user_id: str,
    role: str,
    page: int = 1,
    limit: int = 20,
    trang_thai: Optional[str] = None,
    loai_thu_tuc: Optional[str] = None,
    sort_by: str = "ngay_nop",
    sort_order: str = "desc",
) -> dict:
    """List ho so with pagination and filters."""
    skip = (page - 1) * limit

    # Citizen only sees own ho so
    if role == RoleEnum.citizen.value:
        user_id = current_user_id
    else:
        user_id = None

    # Convert trang_thai string to enum
    trang_thai_enum = None
    if trang_thai:
        try:
            trang_thai_enum = TrangThaiHoSoEnum(trang_thai)
        except ValueError:
            raise BusinessRuleException(f"Trạng thái '{trang_thai}' không hợp lệ")

    total = await ho_so_repo.count_with_filters(
        db, trang_thai=trang_thai_enum, user_id=user_id, loai_thu_tuc=loai_thu_tuc
    )
    items = await ho_so_repo.get_paginated_with_filters(
        db,
        skip=skip,
        limit=limit,
        trang_thai=trang_thai_enum,
        user_id=user_id,
        loai_thu_tuc=loai_thu_tuc,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    return {
        "items": items,
        "pagination": build_pagination(page, limit, total),
    }


async def update_ho_so(
    db: AsyncSession, ho_so_id: str, user_id: str, noi_dung: str
) -> HoSo:
    """Update ho so content. Only allowed in CHO_TIEP_NHAN state."""
    ho_so = await ho_so_repo.get(db, id=ho_so_id)
    if not ho_so:
        raise NotFoundException("Hồ sơ")
    if str(ho_so.user_id) != user_id:
        raise ForbiddenException("Bạn không có quyền cập nhật hồ sơ này")
    if ho_so.trang_thai != TrangThaiHoSoEnum.CHO_TIEP_NHAN:
        raise BusinessRuleException("Chỉ được cập nhật hồ sơ ở trạng thái 'Chờ tiếp nhận'")

    updated = await ho_so_repo.update(db, db_obj=ho_so, obj_in={"noi_dung": noi_dung})
    return updated


async def delete_ho_so(db: AsyncSession, ho_so_id: str, user_id: str) -> None:
    """Delete ho so. Only allowed in CHO_TIEP_NHAN state."""
    ho_so = await ho_so_repo.get(db, id=ho_so_id)
    if not ho_so:
        raise NotFoundException("Hồ sơ")
    if str(ho_so.user_id) != user_id:
        raise ForbiddenException("Bạn không có quyền xoá hồ sơ này")
    if ho_so.trang_thai != TrangThaiHoSoEnum.CHO_TIEP_NHAN:
        raise BusinessRuleException("Chỉ được xoá hồ sơ ở trạng thái 'Chờ tiếp nhận'")

    await ho_so_repo.delete(db, id=ho_so_id)


# ─── Document Upload ─────────────────────────────────────────


async def upload_tai_lieu(
    db: AsyncSession,
    ho_so_id: str,
    user_id: str,
    ten_file: str,
    duong_dan: str,
    loai_file: str,
    kich_thuoc: int,
) -> HoSoTaiLieu:
    """Upload a document for a ho so."""
    ho_so = await ho_so_repo.get(db, id=ho_so_id)
    if not ho_so:
        raise NotFoundException("Hồ sơ")
    if str(ho_so.user_id) != user_id:
        raise ForbiddenException("Bạn không có quyền upload tài liệu cho hồ sơ này")

    tai_lieu = await ho_so_tai_lieu_repo.create(
        db,
        obj_in={
            "id": uuid.uuid4(),
            "ho_so_id": ho_so_id,
            "ten_file": ten_file,
            "duong_dan": duong_dan,
            "loai_file": loai_file,
            "kich_thuoc": kich_thuoc,
        },
    )
    return tai_lieu


# ─── Workflow / State Machine Actions ────────────────────────


async def submit_ho_so(db: AsyncSession, ho_so_id: str, user_id: str) -> HoSo:
    """Submit ho so: CHO_TIEP_NHAN → CHO_XU_LY."""
    ho_so = await ho_so_repo.get(db, id=ho_so_id)
    if not ho_so:
        raise NotFoundException("Hồ sơ")
    if str(ho_so.user_id) != user_id:
        raise ForbiddenException("Bạn không có quyền nộp hồ sơ này")

    next_state = _validate_transition(ho_so, "submit")
    old_state = ho_so.trang_thai.value
    ho_so = await ho_so_repo.update(
        db, db_obj=ho_so, obj_in={"trang_thai": next_state, "ngay_nop": datetime.now(timezone.utc)}
    )
    await _ghi_lich_su(db, ho_so_id, "SUBMIT", old_state, next_state.value, user_id)
    await _notify_status_change(db, ho_so)
    return ho_so


async def tiep_nhan_ho_so(db: AsyncSession, ho_so_id: str, can_bo_id: str) -> HoSo:
    """Receive ho so: CHO_XU_LY → DANG_XU_LY."""
    ho_so = await ho_so_repo.get(db, id=ho_so_id)
    if not ho_so:
        raise NotFoundException("Hồ sơ")

    next_state = _validate_transition(ho_so, "tiep_nhan")
    old_state = ho_so.trang_thai.value
    ho_so = await ho_so_repo.update(
        db,
        db_obj=ho_so,
        obj_in={
            "trang_thai": next_state,
            "nguoi_xu_ly_id": can_bo_id,
            "ngay_xu_ly": datetime.now(timezone.utc),
        },
    )
    await _ghi_lich_su(db, ho_so_id, "TIEP_NHAN", old_state, next_state.value, can_bo_id)
    await _notify_status_change(db, ho_so)
    return ho_so


async def phe_duyet_ho_so(
    db: AsyncSession, ho_so_id: str, can_bo_id: str, ghi_chu: str = ""
) -> HoSo:
    """Approve ho so: DANG_XU_LY → DA_XU_LY."""
    ho_so = await ho_so_repo.get(db, id=ho_so_id)
    if not ho_so:
        raise NotFoundException("Hồ sơ")

    next_state = _validate_transition(ho_so, "phe_duyet")
    old_state = ho_so.trang_thai.value
    ho_so = await ho_so_repo.update(
        db,
        db_obj=ho_so,
        obj_in={
            "trang_thai": next_state,
            "ghi_chu_xu_ly": ghi_chu or None,
            "ngay_xu_ly": datetime.now(timezone.utc),
        },
    )
    await _ghi_lich_su(db, ho_so_id, "PHE_DUYET", old_state, next_state.value, can_bo_id, ghi_chu)
    await _notify_status_change(db, ho_so)
    return ho_so


async def tu_choi_ho_so(
    db: AsyncSession, ho_so_id: str, can_bo_id: str, ly_do: str
) -> HoSo:
    """Reject ho so: DANG_XU_LY → TU_CHOI."""
    if not ly_do:
        raise BusinessRuleException("Vui lòng nhập lý do từ chối")

    ho_so = await ho_so_repo.get(db, id=ho_so_id)
    if not ho_so:
        raise NotFoundException("Hồ sơ")

    next_state = _validate_transition(ho_so, "tu_choi")
    old_state = ho_so.trang_thai.value
    ho_so = await ho_so_repo.update(
        db,
        db_obj=ho_so,
        obj_in={
            "trang_thai": next_state,
            "ly_do_tu_choi": ly_do,
            "ngay_xu_ly": datetime.now(timezone.utc),
        },
    )
    await _ghi_lich_su(db, ho_so_id, "TU_CHOI", old_state, next_state.value, can_bo_id, ly_do)
    await _notify_status_change(db, ho_so)
    return ho_so


async def yeu_cau_bo_sung_ho_so(
    db: AsyncSession, ho_so_id: str, can_bo_id: str, yeu_cau: str
) -> HoSo:
    """Request supplemental documents: DANG_XU_LY → CHO_BO_SUNG."""
    if not yeu_cau:
        raise BusinessRuleException("Vui lòng nhập yêu cầu bổ sung")

    ho_so = await ho_so_repo.get(db, id=ho_so_id)
    if not ho_so:
        raise NotFoundException("Hồ sơ")

    next_state = _validate_transition(ho_so, "yeu_cau_bo_sung")
    old_state = ho_so.trang_thai.value
    ho_so = await ho_so_repo.update(
        db,
        db_obj=ho_so,
        obj_in={"trang_thai": next_state, "yeu_cau_bo_sung": yeu_cau},
    )
    await _ghi_lich_su(
        db, ho_so_id, "YEU_CAU_BO_SUNG", old_state, next_state.value, can_bo_id, yeu_cau
    )
    await _notify_status_change(db, ho_so)
    return ho_so


async def bo_sung_ho_so(db: AsyncSession, ho_so_id: str, user_id: str) -> HoSo:
    """Citizen submits supplemental docs: CHO_BO_SUNG → DA_BO_SUNG."""
    ho_so = await ho_so_repo.get(db, id=ho_so_id)
    if not ho_so:
        raise NotFoundException("Hồ sơ")
    if str(ho_so.user_id) != user_id:
        raise ForbiddenException("Bạn không có quyền thực hiện hành động này")

    next_state = _validate_transition(ho_so, "bo_sung")
    old_state = ho_so.trang_thai.value
    ho_so = await ho_so_repo.update(
        db, db_obj=ho_so, obj_in={"trang_thai": next_state}
    )
    await _ghi_lich_su(db, ho_so_id, "BO_SUNG", old_state, next_state.value, user_id)
    await _notify_status_change(db, ho_so)
    return ho_so


async def nhan_bo_sung_ho_so(
    db: AsyncSession, ho_so_id: str, can_bo_id: str
) -> HoSo:
    """Officer receives supplemental docs: DA_BO_SUNG → DANG_XU_LY."""
    ho_so = await ho_so_repo.get(db, id=ho_so_id)
    if not ho_so:
        raise NotFoundException("Hồ sơ")

    next_state = _validate_transition(ho_so, "nhan_bo_sung")
    old_state = ho_so.trang_thai.value
    ho_so = await ho_so_repo.update(
        db, db_obj=ho_so, obj_in={"trang_thai": next_state}
    )
    await _ghi_lich_su(
        db, ho_so_id, "NHAN_BO_SUNG", old_state, next_state.value, can_bo_id
    )
    await _notify_status_change(db, ho_so)
    return ho_so


# ─── Audit Trail ─────────────────────────────────────────────


async def get_lich_su(db: AsyncSession, ho_so_id: str, user_id: str, role: str) -> list:
    """Get audit trail for a ho so."""
    ho_so = await ho_so_repo.get(db, id=ho_so_id)
    if not ho_so:
        raise NotFoundException("Hồ sơ")

    if role == RoleEnum.citizen.value and str(ho_so.user_id) != user_id:
        raise ForbiddenException("Bạn không có quyền xem lịch sử hồ sơ này")

    return await ho_so_lich_su_repo.get_by_ho_so(db, ho_so_id)
