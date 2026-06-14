"""Test configuration and fixtures."""
import uuid
from datetime import datetime, date, time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from fastapi import FastAPI

from src.models.user import User, RoleEnum, StatusEnum
from src.models.ho_so import HoSo, TrangThaiHoSoEnum
from src.models.ho_so_tai_lieu import HoSoTaiLieu
from src.models.ho_so_lich_su import HoSoLichSu
from src.models.lich_hen import LichHen, TrangThaiLichHenEnum
from src.models.thong_bao import ThongBao, LoaiThongBaoEnum


# ─── Helpers to create mock model instances ─────────────────


def make_user(
    id: str | None = None,
    email: str = "test@govone.vn",
    password_hash: str = "$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5Y7s8e9R0a1b2c3d4e5f6g7h8i",
    ho_ten: str = "Nguyễn Văn A",
    so_cccd: str = "079201000123",
    role: RoleEnum = RoleEnum.citizen,
    trang_thai: StatusEnum = StatusEnum.active,
    refresh_token: str | None = None,
):
    user = MagicMock(spec=User)
    user.id = uuid.UUID(id) if id else uuid.uuid4()
    user.email = email
    user.password_hash = password_hash
    user.ho_ten = ho_ten
    user.so_cccd = so_cccd
    user.so_dien_thoai = "0912345678"
    user.dia_chi = "123 Lê Lợi, Hà Nội"
    user.role = role
    user.trang_thai = trang_thai
    user.refresh_token = refresh_token
    user.created_at = datetime(2026, 1, 1, 0, 0, 0)
    user.updated_at = datetime(2026, 1, 1, 0, 0, 0)

    return user


def make_ho_so(
    id: str | None = None,
    ma_ho_so: str = "HS-2026-0001",
    user_id: str = "00000000-0000-0000-0000-000000000001",
    loai_thu_tuc: str = "cap-giay-phep",
    noi_dung: str = "Xin cấp giấy phép xây dựng",
    trang_thai: TrangThaiHoSoEnum = TrangThaiHoSoEnum.CHO_TIEP_NHAN,
    nguoi_xu_ly_id: str | None = None,
    ghi_chu_xu_ly: str | None = None,
    ly_do_tu_choi: str | None = None,
    yeu_cau_bo_sung: str | None = None,
):
    ho_so = MagicMock(spec=HoSo)
    ho_so.id = uuid.UUID(id) if id else uuid.uuid4()
    ho_so.ma_ho_so = ma_ho_so
    ho_so.user_id = uuid.UUID(user_id)
    ho_so.loai_thu_tuc = loai_thu_tuc
    ho_so.noi_dung = noi_dung
    ho_so.trang_thai = trang_thai
    ho_so.nguoi_xu_ly_id = uuid.UUID(nguoi_xu_ly_id) if nguoi_xu_ly_id else None
    ho_so.ghi_chu_xu_ly = ghi_chu_xu_ly
    ho_so.ly_do_tu_choi = ly_do_tu_choi
    ho_so.yeu_cau_bo_sung = yeu_cau_bo_sung
    ho_so.ngay_nop = datetime.now()
    ho_so.ngay_xu_ly = None
    ho_so.created_at = datetime.now()
    ho_so.updated_at = datetime.now()
    ho_so.tai_lieu = []
    return ho_so


def make_tai_lieu(
    id: str | None = None,
    ho_so_id: str = "00000000-0000-0000-0000-000000000001",
    ten_file: str = "test.pdf",
    duong_dan: str = "/uploads/test.pdf",
    loai_file: str = "application/pdf",
    kich_thuoc: int = 1024,
):
    tl = MagicMock(spec=HoSoTaiLieu)
    tl.id = uuid.UUID(id) if id else uuid.uuid4()
    tl.ho_so_id = uuid.UUID(ho_so_id)
    tl.ten_file = ten_file
    tl.duong_dan = duong_dan
    tl.loai_file = loai_file
    tl.kich_thuoc = kich_thuoc
    tl.created_at = datetime.now()
    return tl


def make_lich_hen(
    id: str | None = None,
    user_id: str = "00000000-0000-0000-0000-000000000001",
    tieu_de: str = "Nộp hồ sơ",
    ngay_hen: date = date(2026, 6, 20),
    gio_hen: time = time(9, 0),
    trang_thai: TrangThaiLichHenEnum = TrangThaiLichHenEnum.CHO_XAC_NHAN,
):
    lh = MagicMock(spec=LichHen)
    lh.id = uuid.UUID(id) if id else uuid.uuid4()
    lh.user_id = uuid.UUID(user_id)
    lh.can_bo_id = None
    lh.tieu_de = tieu_de
    lh.ngay_hen = ngay_hen
    lh.gio_hen = gio_hen
    lh.ghi_chu = None
    lh.trang_thai = trang_thai
    lh.created_at = datetime.now()
    lh.updated_at = datetime.now()
    return lh


def make_thong_bao(
    id: str | None = None,
    user_id: str | None = None,
    tieu_de: str = "Test notification",
    noi_dung: str = "Test content",
    loai: LoaiThongBaoEnum = LoaiThongBaoEnum.he_thong,
    da_doc: bool = False,
):
    tb = MagicMock(spec=ThongBao)
    tb.id = uuid.UUID(id) if id else uuid.uuid4()
    if user_id:
        tb.user_id = uuid.UUID(user_id)
    else:
        tb.user_id = None
    tb.tieu_de = tieu_de
    tb.noi_dung = noi_dung
    tb.loai = loai
    tb.da_doc = da_doc
    tb.created_at = datetime.now()
    return tb


# ─── Async Mock DB session ──────────────────────────────────


@pytest.fixture
def mock_db():
    """Create a mock AsyncSession."""
    db = AsyncMock()
    # Make add/persist do nothing by default
    db.add = MagicMock()
    db.commit = AsyncMock(return_value=None)
    db.refresh = AsyncMock(return_value=None)
    db.rollback = AsyncMock(return_value=None)
    db.execute = AsyncMock()
    return db


# ─── FastAPI test app ────────────────────────────────────────
# (without middleware to keep tests simple)


@pytest.fixture(scope="function")
def test_app():
    """Create a minimal FastAPI app for integration tests."""
    from fastapi import FastAPI
    from src.database.connection import get_db

    app = FastAPI()

    # Register routers only (no middleware)
    from src.api.auth import router as auth_router
    from src.api.ho_so import router as ho_so_router
    from src.api.lich_hen import router as lich_hen_router
    from src.api.thong_bao import router as thong_bao_router

    app.include_router(auth_router)
    app.include_router(ho_so_router)
    app.include_router(lich_hen_router)
    app.include_router(thong_bao_router)

    # Remove the default get_db dependency and replace with override
    return app


@pytest.fixture(scope="function")
def citizen_user():
    return make_user(id="10000000-0000-0000-0000-000000000001", email="citizen@govone.vn")


@pytest.fixture(scope="function")
def officer_user():
    return make_user(
        id="20000000-0000-0000-0000-000000000002",
        email="officer@govone.vn",
        role=RoleEnum.officer,
    )


@pytest.fixture(scope="function")
def admin_user():
    return make_user(
        id="30000000-0000-0000-0000-000000000003",
        email="admin@govone.vn",
        role=RoleEnum.admin,
    )
