"""Tests for ho_so_service — CRUD + state machine workflow."""
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch, ANY

import pytest

from src.middleware.error_handler import (
    BusinessRuleException,
    ForbiddenException,
    NotFoundException,
)
from src.models.ho_so import TrangThaiHoSoEnum
from src.models.user import RoleEnum
from src.services import ho_so_service
from tests.conftest import make_ho_so, make_user, make_tai_lieu


class TestHoSoCRUD:
    @pytest.mark.asyncio
    async def test_create_ho_so(self, mock_db):
        """Should create ho so in CHO_TIEP_NHAN state."""
        user_id = str(uuid.uuid4())
        ho_so = make_ho_so(user_id=user_id, trang_thai=TrangThaiHoSoEnum.CHO_TIEP_NHAN)

        with (
            patch("src.services.ho_so_service.ho_so_repo") as mock_repo,
            patch("src.services.ho_so_service._ghi_lich_su", AsyncMock()),
            patch("src.services.ho_so_service._sinh_ma_ho_so", AsyncMock(return_value="HS-2026-0001")),
        ):
            mock_repo.create = AsyncMock(return_value=ho_so)

            result = await ho_so_service.create_ho_so(
                db=mock_db,
                user_id=user_id,
                loai_thu_tuc="cap-giay-phep",
                noi_dung="Xin cấp phép xây dựng",
            )

            assert result.ma_ho_so == "HS-2026-0001"
            assert result.trang_thai == TrangThaiHoSoEnum.CHO_TIEP_NHAN

    @pytest.mark.asyncio
    async def test_get_ho_so_own(self, mock_db):
        """Citizen can view their own ho so."""
        user_id = str(uuid.uuid4())
        ho_so = make_ho_so(user_id=user_id)

        with patch("src.services.ho_so_service.ho_so_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=ho_so)

            result = await ho_so_service.get_ho_so(
                db=mock_db, ho_so_id=str(ho_so.id),
                current_user_id=user_id, role=RoleEnum.citizen.value,
            )
            assert result.id == ho_so.id

    @pytest.mark.asyncio
    async def test_get_ho_so_other_citizen_raises(self, mock_db):
        """Citizen cannot view another citizen's ho so."""
        ho_so = make_ho_so(user_id=str(uuid.uuid4()))

        with patch("src.services.ho_so_service.ho_so_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=ho_so)

            with pytest.raises(ForbiddenException):
                await ho_so_service.get_ho_so(
                    db=mock_db, ho_so_id=str(ho_so.id),
                    current_user_id=str(uuid.uuid4()), role=RoleEnum.citizen.value,
                )

    @pytest.mark.asyncio
    async def test_get_ho_so_not_found(self, mock_db):
        """Should raise when ho so does not exist."""
        with patch("src.services.ho_so_service.ho_so_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=None)

            with pytest.raises(NotFoundException):
                await ho_so_service.get_ho_so(
                    db=mock_db, ho_so_id=str(uuid.uuid4()),
                    current_user_id=str(uuid.uuid4()), role=RoleEnum.citizen.value,
                )

    @pytest.mark.asyncio
    async def test_list_ho_so_citizen_sees_own(self, mock_db):
        """Citizen list only returns their own ho so."""
        user_id = str(uuid.uuid4())
        ho_so = make_ho_so(user_id=user_id)

        with patch("src.services.ho_so_service.ho_so_repo") as mock_repo:
            mock_repo.count_with_filters = AsyncMock(return_value=1)
            mock_repo.get_paginated_with_filters = AsyncMock(return_value=[ho_so])

            result = await ho_so_service.list_ho_so(
                db=mock_db, current_user_id=user_id,
                role=RoleEnum.citizen.value, page=1, limit=20,
            )
            assert len(result["items"]) == 1
            assert result["pagination"]["total"] == 1

    @pytest.mark.asyncio
    async def test_update_ho_so_only_in_cho_tiep_nhan(self, mock_db):
        """Should only update when state is CHO_TIEP_NHAN."""
        user_id = str(uuid.uuid4())
        ho_so = make_ho_so(user_id=user_id, trang_thai=TrangThaiHoSoEnum.CHO_TIEP_NHAN)

        with patch("src.services.ho_so_service.ho_so_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=ho_so)
            mock_repo.update = AsyncMock(return_value=ho_so)

            result = await ho_so_service.update_ho_so(
                db=mock_db, ho_so_id=str(ho_so.id),
                user_id=user_id, noi_dung="Updated content",
            )
            assert result is not None

    @pytest.mark.asyncio
    async def test_update_ho_so_wrong_state_raises(self, mock_db):
        """Should raise when updating ho so not in CHO_TIEP_NHAN."""
        user_id = str(uuid.uuid4())
        ho_so = make_ho_so(user_id=user_id, trang_thai=TrangThaiHoSoEnum.DANG_XU_LY)

        with patch("src.services.ho_so_service.ho_so_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=ho_so)

            with pytest.raises(BusinessRuleException):
                await ho_so_service.update_ho_so(
                    db=mock_db, ho_so_id=str(ho_so.id),
                    user_id=user_id, noi_dung="Updated content",
                )

    @pytest.mark.asyncio
    async def test_delete_ho_so_only_in_cho_tiep_nhan(self, mock_db):
        """Should only delete when state is CHO_TIEP_NHAN."""
        user_id = str(uuid.uuid4())
        ho_so = make_ho_so(user_id=user_id, trang_thai=TrangThaiHoSoEnum.CHO_TIEP_NHAN)

        with patch("src.services.ho_so_service.ho_so_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=ho_so)
            mock_repo.delete = AsyncMock(return_value=ho_so)

            await ho_so_service.delete_ho_so(
                db=mock_db, ho_so_id=str(ho_so.id), user_id=user_id,
            )
            mock_repo.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_upload_tai_lieu(self, mock_db):
        """Should create HoSoTaiLieu record."""
        user_id = str(uuid.uuid4())
        ho_so = make_ho_so(user_id=user_id)
        tai_lieu = make_tai_lieu(ho_so_id=str(ho_so.id))

        with (
            patch("src.services.ho_so_service.ho_so_repo") as mock_ho_so_repo,
            patch("src.services.ho_so_service.ho_so_tai_lieu_repo") as mock_tl_repo,
        ):
            mock_ho_so_repo.get = AsyncMock(return_value=ho_so)
            mock_tl_repo.create = AsyncMock(return_value=tai_lieu)

            result = await ho_so_service.upload_tai_lieu(
                db=mock_db, ho_so_id=str(ho_so.id), user_id=user_id,
                ten_file="test.pdf", duong_dan="/uploads/test.pdf",
                loai_file="application/pdf", kich_thuoc=1024,
            )
            assert result.ten_file == "test.pdf"


class TestStateMachine:
    """Test all state transitions for the ho so workflow."""

    @pytest.mark.asyncio
    async def test_submit_cho_tiep_nhan_to_cho_xu_ly(self, mock_db):
        """CHO_TIEP_NHAN → CHO_XU_LY: citizen submits."""
        user_id = str(uuid.uuid4())
        ho_so = make_ho_so(user_id=user_id, trang_thai=TrangThaiHoSoEnum.CHO_TIEP_NHAN)

        with (
            patch("src.services.ho_so_service.ho_so_repo") as mock_repo,
            patch("src.services.ho_so_service._ghi_lich_su", AsyncMock()),
            patch("src.services.ho_so_service._notify_status_change", AsyncMock()),
        ):
            mock_repo.get = AsyncMock(return_value=ho_so)
            mock_repo.update = AsyncMock(return_value=make_ho_so(
                user_id=user_id, trang_thai=TrangThaiHoSoEnum.CHO_XU_LY,
            ))

            result = await ho_so_service.submit_ho_so(
                db=mock_db, ho_so_id=str(ho_so.id), user_id=user_id,
            )
            assert result.trang_thai == TrangThaiHoSoEnum.CHO_XU_LY

    @pytest.mark.asyncio
    async def test_submit_wrong_user_raises(self, mock_db):
        """Only the owner can submit their ho so."""
        ho_so = make_ho_so(user_id=str(uuid.uuid4()))

        with patch("src.services.ho_so_service.ho_so_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=ho_so)

            with pytest.raises(ForbiddenException):
                await ho_so_service.submit_ho_so(
                    db=mock_db, ho_so_id=str(ho_so.id), user_id=str(uuid.uuid4()),
                )

    @pytest.mark.asyncio
    async def test_tiep_nhan_cho_xu_ly_to_dang_xu_ly(self, mock_db):
        """CHO_XU_LY → DANG_XU_LY: officer receives."""
        can_bo_id = str(uuid.uuid4())
        ho_so = make_ho_so(trang_thai=TrangThaiHoSoEnum.CHO_XU_LY)

        with (
            patch("src.services.ho_so_service.ho_so_repo") as mock_repo,
            patch("src.services.ho_so_service._ghi_lich_su", AsyncMock()),
            patch("src.services.ho_so_service._notify_status_change", AsyncMock()),
        ):
            mock_repo.get = AsyncMock(return_value=ho_so)
            mock_repo.update = AsyncMock(return_value=make_ho_so(
                trang_thai=TrangThaiHoSoEnum.DANG_XU_LY, nguoi_xu_ly_id=can_bo_id,
            ))

            result = await ho_so_service.tiep_nhan_ho_so(
                db=mock_db, ho_so_id=str(ho_so.id), can_bo_id=can_bo_id,
            )
            assert result.trang_thai == TrangThaiHoSoEnum.DANG_XU_LY

    @pytest.mark.asyncio
    async def test_phe_duyet_dang_xu_ly_to_da_xu_ly(self, mock_db):
        """DANG_XU_LY → DA_XU_LY: officer approves."""
        can_bo_id = str(uuid.uuid4())
        ho_so = make_ho_so(trang_thai=TrangThaiHoSoEnum.DANG_XU_LY)

        with (
            patch("src.services.ho_so_service.ho_so_repo") as mock_repo,
            patch("src.services.ho_so_service._ghi_lich_su", AsyncMock()),
            patch("src.services.ho_so_service._notify_status_change", AsyncMock()),
        ):
            mock_repo.get = AsyncMock(return_value=ho_so)
            mock_repo.update = AsyncMock(return_value=make_ho_so(
                trang_thai=TrangThaiHoSoEnum.DA_XU_LY,
            ))

            result = await ho_so_service.phe_duyet_ho_so(
                db=mock_db, ho_so_id=str(ho_so.id),
                can_bo_id=can_bo_id, ghi_chu="Hợp lệ",
            )
            assert result.trang_thai == TrangThaiHoSoEnum.DA_XU_LY

    @pytest.mark.asyncio
    async def test_tu_choi_dang_xu_ly_to_tu_choi(self, mock_db):
        """DANG_XU_LY → TU_CHOI: officer rejects with reason."""
        can_bo_id = str(uuid.uuid4())
        ho_so = make_ho_so(trang_thai=TrangThaiHoSoEnum.DANG_XU_LY)

        with (
            patch("src.services.ho_so_service.ho_so_repo") as mock_repo,
            patch("src.services.ho_so_service._ghi_lich_su", AsyncMock()),
            patch("src.services.ho_so_service._notify_status_change", AsyncMock()),
        ):
            mock_repo.get = AsyncMock(return_value=ho_so)
            mock_repo.update = AsyncMock(return_value=make_ho_so(
                trang_thai=TrangThaiHoSoEnum.TU_CHOI, ly_do_tu_choi="Thiếu giấy tờ",
            ))

            result = await ho_so_service.tu_choi_ho_so(
                db=mock_db, ho_so_id=str(ho_so.id),
                can_bo_id=can_bo_id, ly_do="Thiếu giấy tờ",
            )
            assert result.trang_thai == TrangThaiHoSoEnum.TU_CHOI

    @pytest.mark.asyncio
    async def test_tu_choi_without_reason_raises(self, mock_db):
        """Rejection must include a reason."""
        ho_so = make_ho_so(trang_thai=TrangThaiHoSoEnum.DANG_XU_LY)

        with patch("src.services.ho_so_service.ho_so_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=ho_so)
            with pytest.raises(BusinessRuleException) as exc:
                await ho_so_service.tu_choi_ho_so(
                    db=mock_db, ho_so_id=str(ho_so.id),
                    can_bo_id=str(uuid.uuid4()), ly_do="",
                )
            assert "lý do từ chối" in str(exc.value.message)

    @pytest.mark.asyncio
    async def test_yeu_cau_bo_sung_dang_xu_ly_to_cho_bo_sung(self, mock_db):
        """DANG_XU_LY → CHO_BO_SUNG: officer requests supplements."""
        can_bo_id = str(uuid.uuid4())
        ho_so = make_ho_so(trang_thai=TrangThaiHoSoEnum.DANG_XU_LY)

        with (
            patch("src.services.ho_so_service.ho_so_repo") as mock_repo,
            patch("src.services.ho_so_service._ghi_lich_su", AsyncMock()),
            patch("src.services.ho_so_service._notify_status_change", AsyncMock()),
        ):
            mock_repo.get = AsyncMock(return_value=ho_so)
            mock_repo.update = AsyncMock(return_value=make_ho_so(
                trang_thai=TrangThaiHoSoEnum.CHO_BO_SUNG,
                yeu_cau_bo_sung="Cần bổ sung CCCD",
            ))

            result = await ho_so_service.yeu_cau_bo_sung_ho_so(
                db=mock_db, ho_so_id=str(ho_so.id),
                can_bo_id=can_bo_id, yeu_cau="Cần bổ sung CCCD",
            )
            assert result.trang_thai == TrangThaiHoSoEnum.CHO_BO_SUNG

    @pytest.mark.asyncio
    async def test_yeu_cau_bo_sung_empty_raises(self, mock_db):
        """Supplement request must include details."""
        ho_so = make_ho_so(trang_thai=TrangThaiHoSoEnum.DANG_XU_LY)

        with patch("src.services.ho_so_service.ho_so_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=ho_so)
            with pytest.raises(BusinessRuleException) as exc:
                await ho_so_service.yeu_cau_bo_sung_ho_so(
                    db=mock_db, ho_so_id=str(ho_so.id),
                    can_bo_id=str(uuid.uuid4()), yeu_cau="",
                )
            assert "bổ sung" in str(exc.value.message)

    @pytest.mark.asyncio
    async def test_bo_sung_cho_bo_sung_to_da_bo_sung(self, mock_db):
        """CHO_BO_SUNG → DA_BO_SUNG: citizen supplements."""
        user_id = str(uuid.uuid4())
        ho_so = make_ho_so(user_id=user_id, trang_thai=TrangThaiHoSoEnum.CHO_BO_SUNG)

        with (
            patch("src.services.ho_so_service.ho_so_repo") as mock_repo,
            patch("src.services.ho_so_service._ghi_lich_su", AsyncMock()),
            patch("src.services.ho_so_service._notify_status_change", AsyncMock()),
        ):
            mock_repo.get = AsyncMock(return_value=ho_so)
            mock_repo.update = AsyncMock(return_value=make_ho_so(
                user_id=user_id, trang_thai=TrangThaiHoSoEnum.DA_BO_SUNG,
            ))

            result = await ho_so_service.bo_sung_ho_so(
                db=mock_db, ho_so_id=str(ho_so.id), user_id=user_id,
            )
            assert result.trang_thai == TrangThaiHoSoEnum.DA_BO_SUNG

    @pytest.mark.asyncio
    async def test_nhan_bo_sung_da_bo_sung_to_dang_xu_ly(self, mock_db):
        """DA_BO_SUNG → DANG_XU_LY: officer receives supplements."""
        can_bo_id = str(uuid.uuid4())
        ho_so = make_ho_so(trang_thai=TrangThaiHoSoEnum.DA_BO_SUNG)

        with (
            patch("src.services.ho_so_service.ho_so_repo") as mock_repo,
            patch("src.services.ho_so_service._ghi_lich_su", AsyncMock()),
            patch("src.services.ho_so_service._notify_status_change", AsyncMock()),
        ):
            mock_repo.get = AsyncMock(return_value=ho_so)
            mock_repo.update = AsyncMock(return_value=make_ho_so(
                trang_thai=TrangThaiHoSoEnum.DANG_XU_LY,
            ))

            result = await ho_so_service.nhan_bo_sung_ho_so(
                db=mock_db, ho_so_id=str(ho_so.id), can_bo_id=can_bo_id,
            )
            assert result.trang_thai == TrangThaiHoSoEnum.DANG_XU_LY

    @pytest.mark.asyncio
    async def test_invalid_transition_raises(self, mock_db):
        """Should raise when action is not valid for current state."""
        ho_so = make_ho_so(trang_thai=TrangThaiHoSoEnum.CHO_XU_LY)

        with patch("src.services.ho_so_service.ho_so_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=ho_so)

            with pytest.raises(BusinessRuleException) as exc:
                await ho_so_service.phe_duyet_ho_so(
                    db=mock_db, ho_so_id=str(ho_so.id),
                    can_bo_id=str(uuid.uuid4()),
                )
            # Can't approve from CHO_XU_LY — must be DANG_XU_LY
            assert "phe_duyet" in str(exc.value.message)

    @pytest.mark.asyncio
    async def test_submit_from_dang_xu_ly_raises(self, mock_db):
        """Submit is only valid from CHO_TIEP_NHAN."""
        user_id = str(uuid.uuid4())
        ho_so = make_ho_so(user_id=user_id, trang_thai=TrangThaiHoSoEnum.DANG_XU_LY)

        with patch("src.services.ho_so_service.ho_so_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=ho_so)

            with pytest.raises(BusinessRuleException):
                await ho_so_service.submit_ho_so(
                    db=mock_db, ho_so_id=str(ho_so.id),
                    user_id=user_id,  # same owner, but wrong state
                )


class TestAuditTrail:
    @pytest.mark.asyncio
    async def test_ghi_lich_su_creates_record(self, mock_db):
        """_ghi_lich_su should create a HoSoLichSu record."""
        with patch("src.services.ho_so_service.ho_so_lich_su_repo") as mock_repo:
            mock_repo.create = AsyncMock(return_value=MagicMock())

            from src.services.ho_so_service import _ghi_lich_su
            result = await _ghi_lich_su(
                db=mock_db, ho_so_id=str(uuid.uuid4()),
                hanh_dong="TEST", trang_thai_cu="A",
                trang_thai_moi="B", nguoi_thuc_hien_id=str(uuid.uuid4()),
            )
            assert result is not None

    @pytest.mark.asyncio
    async def test_get_lich_su_not_found_raises(self, mock_db):
        """Should raise when ho so does not exist."""
        with patch("src.services.ho_so_service.ho_so_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=None)

            with pytest.raises(NotFoundException):
                await ho_so_service.get_lich_su(
                    db=mock_db, ho_so_id=str(uuid.uuid4()),
                    user_id=str(uuid.uuid4()), role=RoleEnum.citizen.value,
                )


class TestMaHoSoGeneration:
    @pytest.mark.asyncio
    async def test_sinh_ma_ho_so(self, mock_db):
        """Should generate HS-YYYY-XXXX format."""
        from sqlalchemy import select, func
        from src.models.ho_so import HoSo

        # Mock the execute to return count=41
        mock_result = MagicMock()
        mock_result.scalar.return_value = 41
        mock_db.execute = AsyncMock(return_value=mock_result)

        ma = await ho_so_service._sinh_ma_ho_so(mock_db)
        assert ma.startswith("HS-2026-")
        assert ma == "HS-2026-0042"
        assert ma == "HS-2026-0042"


class TestTransitionRules:
    """Verify the TRANSITIONS mapping covers expected rules."""

    def test_all_states_have_defined_transitions(self):
        """Every state except terminal states should have transitions."""
        states_with_transitions = set(ho_so_service.TRANSITIONS.keys())
        terminal_states = {
            TrangThaiHoSoEnum.DA_XU_LY,
            TrangThaiHoSoEnum.TU_CHOI,
        }
        all_states = set(TrangThaiHoSoEnum)
        non_terminal = all_states - terminal_states
        assert non_terminal == states_with_transitions, (
            f"Missing transitions for: {non_terminal - states_with_transitions}"
        )

    def test_transition_labels_use_vietnamese(self):
        """Transition labels should be readable business actions."""
        assert "phe_duyet" in ho_so_service.TRANSITIONS[TrangThaiHoSoEnum.DANG_XU_LY]
        assert "tu_choi" in ho_so_service.TRANSITIONS[TrangThaiHoSoEnum.DANG_XU_LY]
        assert "yeu_cau_bo_sung" in ho_so_service.TRANSITIONS[TrangThaiHoSoEnum.DANG_XU_LY]
        assert "bo_sung" in ho_so_service.TRANSITIONS[TrangThaiHoSoEnum.CHO_BO_SUNG]
