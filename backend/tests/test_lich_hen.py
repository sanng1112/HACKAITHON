"""Tests for lich_hen_service — CRUD + conflict detection."""
import uuid
from datetime import date, datetime, time, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.middleware.error_handler import (
    BusinessRuleException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
)
from src.models.lich_hen import TrangThaiLichHenEnum
from src.models.user import RoleEnum
from src.services import lich_hen_service
from tests.conftest import make_lich_hen, make_user


class TestLichHenCRUD:
    @pytest.mark.asyncio
    async def test_create_lich_hen_no_conflict(self, mock_db):
        """Should create appointment when no conflict at the same time."""
        user_id = str(uuid.uuid4())
        lich_hen = make_lich_hen(user_id=user_id)

        with patch("src.services.lich_hen_service.lich_hen_repo") as mock_repo:
            mock_repo.check_conflict = AsyncMock(return_value=False)
            mock_repo.create = AsyncMock(return_value=lich_hen)

            result = await lich_hen_service.create_lich_hen(
                db=mock_db, user_id=user_id,
                tieu_de="Nộp hồ sơ", ngay_hen=date(2026, 6, 20),
                gio_hen=time(9, 0),
            )
            assert result.tieu_de == "Nộp hồ sơ"
            assert result.trang_thai == TrangThaiLichHenEnum.CHO_XAC_NHAN

    @pytest.mark.asyncio
    async def test_create_lich_hen_with_conflict(self, mock_db):
        """Should raise SCHEDULE_CONFLICT when time slot is taken."""
        with patch("src.services.lich_hen_service.lich_hen_repo") as mock_repo:
            mock_repo.check_conflict = AsyncMock(return_value=True)

            with pytest.raises(ConflictException) as exc:
                await lich_hen_service.create_lich_hen(
                    db=mock_db, user_id=str(uuid.uuid4()),
                    tieu_de="Nộp hồ sơ", ngay_hen=date(2026, 6, 20),
                    gio_hen=time(9, 0),
                )
            assert exc.value.code == "SCHEDULE_CONFLICT"

    @pytest.mark.asyncio
    async def test_get_lich_hen_own(self, mock_db):
        """Citizen can view their own appointment."""
        user_id = str(uuid.uuid4())
        lh = make_lich_hen(user_id=user_id)

        with patch("src.services.lich_hen_service.lich_hen_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=lh)

            result = await lich_hen_service.get_lich_hen(
                db=mock_db, lich_hen_id=str(lh.id),
                current_user_id=user_id, role=RoleEnum.citizen.value,
            )
            assert result.id == lh.id

    @pytest.mark.asyncio
    async def test_get_lich_hen_other_raises(self, mock_db):
        """Citizen cannot view another's appointment."""
        lh = make_lich_hen(user_id=str(uuid.uuid4()))

        with patch("src.services.lich_hen_service.lich_hen_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=lh)

            with pytest.raises(ForbiddenException):
                await lich_hen_service.get_lich_hen(
                    db=mock_db, lich_hen_id=str(lh.id),
                    current_user_id=str(uuid.uuid4()),
                    role=RoleEnum.citizen.value,
                )

    @pytest.mark.asyncio
    async def test_get_lich_hen_not_found(self, mock_db):
        """Should raise when not found."""
        with patch("src.services.lich_hen_service.lich_hen_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=None)

            with pytest.raises(NotFoundException):
                await lich_hen_service.get_lich_hen(
                    db=mock_db, lich_hen_id=str(uuid.uuid4()),
                    current_user_id=str(uuid.uuid4()),
                    role=RoleEnum.citizen.value,
                )

    @pytest.mark.asyncio
    async def test_list_lich_hen_citizen(self, mock_db):
        """Citizen list only returns their own appointments."""
        user_id = str(uuid.uuid4())
        lh = make_lich_hen(user_id=user_id)

        with patch("src.services.lich_hen_service.lich_hen_repo") as mock_repo:
            mock_repo.get_paginated_with_filters = AsyncMock(
                return_value=([lh], 1)
            )

            result = await lich_hen_service.list_lich_hen(
                db=mock_db, current_user_id=user_id,
                role=RoleEnum.citizen.value, page=1, limit=20,
            )
            assert len(result["items"]) == 1

    @pytest.mark.asyncio
    async def test_update_lich_hen_as_owner(self, mock_db):
        """Owner can update appointment status."""
        user_id = str(uuid.uuid4())
        lh = make_lich_hen(user_id=user_id)

        with patch("src.services.lich_hen_service.lich_hen_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=lh)
            mock_repo.update = AsyncMock(return_value=lh)

            result = await lich_hen_service.update_lich_hen(
                db=mock_db, lich_hen_id=str(lh.id),
                current_user_id=user_id, role=RoleEnum.citizen.value,
                trang_thai="DA_HUY",
            )
            assert result is not None


class TestDeleteLichHen:
    @pytest.mark.asyncio
    async def test_delete_more_than_24h_before(self, mock_db):
        """Should allow cancel if > 24h before appointment."""
        user_id = str(uuid.uuid4())
        # Appointment in 48 hours
        future_date = (datetime.now(timezone.utc) + timedelta(hours=48)).date()
        future_time = time(10, 0)
        lh = make_lich_hen(
            user_id=user_id, ngay_hen=future_date, gio_hen=future_time,
        )

        with patch("src.services.lich_hen_service.lich_hen_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=lh)
            mock_repo.update = AsyncMock(return_value=lh)

            await lich_hen_service.delete_lich_hen(
                db=mock_db, lich_hen_id=str(lh.id), user_id=user_id,
            )
            mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_less_than_24h_raises(self, mock_db):
        """Should raise when cancelling within 24h of appointment."""
        user_id = str(uuid.uuid4())
        # Appointment in 2 hours
        near_future = (datetime.now(timezone.utc) + timedelta(hours=2)).date()
        lh = make_lich_hen(user_id=user_id, ngay_hen=near_future, gio_hen=time(10, 0))

        with patch("src.services.lich_hen_service.lich_hen_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=lh)

            with pytest.raises(BusinessRuleException) as exc:
                await lich_hen_service.delete_lich_hen(
                    db=mock_db, lich_hen_id=str(lh.id), user_id=user_id,
                )
            assert "24 giờ" in str(exc.value.message)

    @pytest.mark.asyncio
    async def test_delete_wrong_owner_raises(self, mock_db):
        """Should raise when non-owner tries to cancel."""
        lh = make_lich_hen()

        with patch("src.services.lich_hen_service.lich_hen_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=lh)

            with pytest.raises(ForbiddenException):
                await lich_hen_service.delete_lich_hen(
                    db=mock_db, lich_hen_id=str(lh.id),
                    user_id=str(uuid.uuid4()),
                )
