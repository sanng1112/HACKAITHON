"""Tests for auth_service and auth API."""
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import jwt as pyjwt
import pytest
from pytest import approx

from src.config.settings import settings
from src.middleware.error_handler import AppException, UnauthorizedException, ConflictException
from src.models.user import RoleEnum, StatusEnum
from src.services import auth_service
from src.utils.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from tests.conftest import make_user


# ─── Unit tests: Security utils ─────────────────────────────


class TestSecurityUtils:
    def test_hash_and_verify_password(self):
        hashed = hash_password("securePass123!")
        assert verify_password("securePass123!", hashed)
        assert not verify_password("wrongPass!", hashed)

    def test_create_and_decode_access_token(self):
        data = {"sub": "user-1", "role": "citizen"}
        token = create_access_token(data)
        payload = decode_token(token)
        assert payload["sub"] == "user-1"
        assert payload["role"] == "citizen"
        assert payload["type"] == "access"
        assert "exp" in payload

    def test_create_and_decode_refresh_token(self):
        data = {"sub": "user-1"}
        token = create_refresh_token(data)
        payload = decode_token(token)
        assert payload["sub"] == "user-1"
        assert payload["type"] == "refresh"

    def test_expired_token_raises(self):
        import datetime
        from src.utils.security import create_access_token
        data = {"sub": "user-1"}
        token = create_access_token(
            data,
            expires_delta=datetime.timedelta(seconds=-1),  # already expired
        )
        with pytest.raises(pyjwt.ExpiredSignatureError):
            decode_token(token)

    def test_invalid_token_raises(self):
        with pytest.raises(pyjwt.InvalidTokenError):
            decode_token("invalid.token.here")


# ─── Unit tests: Auth Service ───────────────────────────────


class TestAuthService:
    @pytest.mark.asyncio
    async def test_register_success(self, mock_db):
        """Should create user with hashed password and citizen role."""
        mock_db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=None)))
        mock_db.execute = AsyncMock(return_value=MagicMock(scalar=MagicMock(return_value=None)))

        user = make_user(id=str(uuid.uuid4()))
        with patch("src.services.auth_service.user_repo") as mock_repo:
            mock_repo.get_by_email = AsyncMock(return_value=None)
            mock_repo.get_by_cccd = AsyncMock(return_value=None)
            mock_repo.create = AsyncMock(return_value=user)

            result = await auth_service.register(
                db=mock_db,
                email="new@govone.vn",
                password="password123",
                ho_ten="Nguyễn Văn B",
                so_cccd="079202000456",
            )

            assert result.ho_ten == "Nguyễn Văn A"

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, mock_db):
        """Should raise EMAIL_EXISTS when email is taken."""
        existing_user = make_user()
        with patch("src.services.auth_service.user_repo") as mock_repo:
            mock_repo.get_by_email = AsyncMock(return_value=existing_user)

            with pytest.raises(ConflictException) as exc:
                await auth_service.register(
                    db=mock_db,
                    email="existing@govone.vn",
                    password="password123",
                    ho_ten="Test",
                    so_cccd="079202000456",
                )
            assert exc.value.code == "EMAIL_EXISTS"

    @pytest.mark.asyncio
    async def test_register_duplicate_cccd(self, mock_db):
        """Should raise CCCD_EXISTS when CCCD is taken."""
        with patch("src.services.auth_service.user_repo") as mock_repo:
            mock_repo.get_by_email = AsyncMock(return_value=None)
            mock_repo.get_by_cccd = AsyncMock(
                return_value=make_user(email="other@govone.vn")
            )

            with pytest.raises(ConflictException) as exc:
                await auth_service.register(
                    db=mock_db,
                    email="new@govone.vn",
                    password="password123",
                    ho_ten="Test",
                    so_cccd="079202000456",
                )
            assert exc.value.code == "CCCD_EXISTS"

    @pytest.mark.asyncio
    async def test_login_success(self, mock_db):
        """Should return token pair with user info."""
        hashed = hash_password("correctpass")
        user = make_user(password_hash=hashed)

        with patch("src.services.auth_service.user_repo") as mock_repo:
            mock_repo.get_by_email = AsyncMock(return_value=user)
            mock_repo.update = AsyncMock(return_value=user)

            result = await auth_service.login(
                db=mock_db, email="test@govone.vn", password="correctpass"
            )

            assert "access_token" in result
            assert "refresh_token" in result
            assert result["token_type"] == "bearer"
            assert result["user"]["email"] == "test@govone.vn"
            assert result["user"]["role"] == "citizen"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, mock_db):
        """Should raise UNAUTHORIZED on wrong password."""
        hashed = hash_password("correctpass")
        user = make_user(password_hash=hashed)

        with patch("src.services.auth_service.user_repo") as mock_repo:
            mock_repo.get_by_email = AsyncMock(return_value=user)

            with pytest.raises(UnauthorizedException):
                await auth_service.login(
                    db=mock_db, email="test@govone.vn", password="wrongpass"
                )

    @pytest.mark.asyncio
    async def test_login_inactive_user(self, mock_db):
        """Should raise UNAUTHORIZED if account is locked."""
        hashed = hash_password("correctpass")
        user = make_user(password_hash=hashed, trang_thai=StatusEnum.locked)

        with patch("src.services.auth_service.user_repo") as mock_repo:
            mock_repo.get_by_email = AsyncMock(return_value=user)

            with pytest.raises(UnauthorizedException) as exc:
                await auth_service.login(
                    db=mock_db, email="test@govone.vn", password="correctpass"
                )
            assert "khoá" in str(exc.value.message)

    @pytest.mark.asyncio
    async def test_refresh_token_success(self, mock_db):
        """Should issue new token pair from valid refresh token."""
        user = make_user()
        token = create_refresh_token({"sub": str(user.id), "role": "citizen"})
        user.refresh_token = token

        with patch("src.services.auth_service.user_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=user)
            mock_repo.update = AsyncMock(return_value=user)

            result = await auth_service.refresh_token(db=mock_db, token=token)
            assert "access_token" in result
            assert "refresh_token" in result

    @pytest.mark.asyncio
    async def test_refresh_token_expired(self, mock_db):
        """Should raise on expired refresh token."""
        import datetime
        token = create_refresh_token(
            {"sub": "user-1"},
            expires_delta=datetime.timedelta(seconds=-1),
        )

        with pytest.raises(UnauthorizedException):
            await auth_service.refresh_token(db=mock_db, token=token)

    @pytest.mark.asyncio
    async def test_refresh_token_wrong_type(self, mock_db):
        """Should raise if token is access-type, not refresh."""
        token = create_access_token({"sub": "user-1", "role": "citizen"})
        with pytest.raises(UnauthorizedException):
            await auth_service.refresh_token(db=mock_db, token=token)

    @pytest.mark.asyncio
    async def test_change_password_success(self, mock_db):
        """Should update password hash after verifying current password."""
        hashed = hash_password("oldpass")
        user = make_user(password_hash=hashed)

        with patch("src.services.auth_service.user_repo") as mock_repo:
            mock_repo.update = AsyncMock(return_value=user)
            await auth_service.change_password(
                db=mock_db, user=user, current_password="oldpass", new_password="newpass"
            )
            mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_change_password_wrong_current(self, mock_db):
        """Should raise if current password is wrong."""
        hashed = hash_password("oldpass")
        user = make_user(password_hash=hashed)

        with pytest.raises(UnauthorizedException):
            await auth_service.change_password(
                db=mock_db, user=user, current_password="wrong", new_password="newpass"
            )

    @pytest.mark.asyncio
    async def test_logout_clears_refresh_token(self, mock_db):
        """Should clear refresh_token on logout."""
        user = make_user(refresh_token="some-token")

        with patch("src.services.auth_service.user_repo") as mock_repo:
            mock_repo.update = AsyncMock(return_value=user)
            await auth_service.logout(db=mock_db, user=user)
            mock_repo.update.assert_called_once_with(
                mock_db, db_obj=user, obj_in={"refresh_token": None}
            )

    @pytest.mark.asyncio
    async def test_get_current_user_found(self, mock_db):
        """Should return user when exists."""
        user = make_user()
        with patch("src.services.auth_service.user_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=user)
            result = await auth_service.get_current_user(mock_db, str(user.id))
            assert result.id == user.id

    @pytest.mark.asyncio
    async def test_get_current_user_not_found(self, mock_db):
        """Should raise when user does not exist."""
        with patch("src.services.auth_service.user_repo") as mock_repo:
            mock_repo.get = AsyncMock(return_value=None)
            with pytest.raises(UnauthorizedException):
                await auth_service.get_current_user(mock_db, str(uuid.uuid4()))
