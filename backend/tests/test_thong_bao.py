"""Tests for thong_bao_service — notification CRUD."""
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.middleware.error_handler import BusinessRuleException, NotFoundException
from src.models.thong_bao import LoaiThongBaoEnum
from src.services import thong_bao_service
from tests.conftest import make_thong_bao


class TestThongBaoCreate:
    @pytest.mark.asyncio
    async def test_create_notification(self, mock_db):
        """Should create a personal notification."""
        user_id = str(uuid.uuid4())
        tb = make_thong_bao(user_id=user_id)

        with patch("src.services.thong_bao_service.thong_bao_repo") as mock_repo:
            mock_repo.create = AsyncMock(return_value=tb)

            result = await thong_bao_service.create_notification(
                db=mock_db, user_id=user_id,
                tieu_de="Test", noi_dung="Test content", loai="he_thong",
            )
            assert result.tieu_de == "Test notification"
            assert result.loai == LoaiThongBaoEnum.he_thong

    @pytest.mark.asyncio
    async def test_create_broadcast_notification(self, mock_db):
        """Should create broadcast (user_id=None)."""
        tb = make_thong_bao(user_id=None)

        with patch("src.services.thong_bao_service.thong_bao_repo") as mock_repo:
            mock_repo.create = AsyncMock(return_value=tb)

            result = await thong_bao_service.create_notification(
                db=mock_db, user_id=None,
                tieu_de="Broadcast", noi_dung="To all", loai="he_thong",
            )
            assert result.user_id is None

    @pytest.mark.asyncio
    async def test_create_invalid_loai_raises(self, mock_db):
        """Should raise on invalid notification type."""
        with pytest.raises(BusinessRuleException):
            await thong_bao_service.create_notification(
                db=mock_db, user_id=str(uuid.uuid4()),
                tieu_de="Test", noi_dung="Test", loai="invalid_type",
            )


class TestThongBaoList:
    @pytest.mark.asyncio
    async def test_list_notifications_includes_broadcast(self, mock_db):
        """Notifications list includes both personal and broadcast."""
        user_id = str(uuid.uuid4())
        tb1 = make_thong_bao(user_id=user_id, tieu_de="Personal")
        tb2 = make_thong_bao(user_id=None, tieu_de="Broadcast")
        expected_tbs = [tb1, tb2]

        with patch("src.services.thong_bao_service.thong_bao_repo") as mock_repo:
            mock_repo.get_paginated_for_user = AsyncMock(
                return_value=(expected_tbs, 2)
            )

            result = await thong_bao_service.list_notifications(
                db=mock_db, user_id=user_id, page=1, limit=20,
            )
            assert len(result["items"]) == 2
            assert result["pagination"]["total"] == 2

    @pytest.mark.asyncio
    async def test_list_notifications_filter_by_da_doc(self, mock_db):
        """Should filter by read status."""
        user_id = str(uuid.uuid4())

        with patch("src.services.thong_bao_service.thong_bao_repo") as mock_repo:
            mock_repo.get_paginated_for_user = AsyncMock(
                return_value=([], 0)
            )

            result = await thong_bao_service.list_notifications(
                db=mock_db, user_id=user_id, page=1, limit=20, da_doc=False,
            )
            assert len(result["items"]) == 0
            # Verify filter was passed
            mock_repo.get_paginated_for_user.assert_called_with(
                mock_db, user_id=user_id, skip=0, limit=20,
                da_doc=False, loai=None,
            )


class TestThongBaoMarkRead:
    @pytest.mark.asyncio
    async def test_mark_as_read(self, mock_db):
        """Should mark notification as read."""
        user_id = str(uuid.uuid4())
        tb = make_thong_bao(user_id=user_id, da_doc=False)

        with patch("src.services.thong_bao_service.thong_bao_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=tb)
            mock_repo.update = AsyncMock(return_value=make_thong_bao(user_id=user_id, da_doc=True))

            result = await thong_bao_service.mark_as_read(
                db=mock_db, thong_bao_id=str(tb.id), user_id=user_id,
            )
            # The returned mock has da_doc set
            mock_repo.update.assert_called_once_with(
                mock_db, db_obj=tb, obj_in={"da_doc": True}
            )

    @pytest.mark.asyncio
    async def test_mark_as_read_not_found(self, mock_db):
        """Should raise on non-existent notification."""
        with patch("src.services.thong_bao_service.thong_bao_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=None)

            with pytest.raises(NotFoundException):
                await thong_bao_service.mark_as_read(
                    db=mock_db, thong_bao_id=str(uuid.uuid4()),
                    user_id=str(uuid.uuid4()),
                )

    @pytest.mark.asyncio
    async def test_mark_other_users_notification_raises(self, mock_db):
        """Should raise when trying to mark another user's notification."""
        tb = make_thong_bao(user_id=str(uuid.uuid4()))

        with patch("src.services.thong_bao_service.thong_bao_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=tb)

            with pytest.raises(NotFoundException):
                await thong_bao_service.mark_as_read(
                    db=mock_db, thong_bao_id=str(tb.id),
                    user_id=str(uuid.uuid4()),
                )
