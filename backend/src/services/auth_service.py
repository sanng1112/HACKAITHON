"""Authentication & authorization service."""
import uuid
from typing import Optional

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.database.repositories.user_repository import user_repo
from src.middleware.error_handler import (
    AppException,
    ConflictException,
    UnauthorizedException,
)
from src.models.user import RoleEnum, StatusEnum, User
from src.utils.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


async def register(
    db: AsyncSession,
    email: str,
    password: str,
    ho_ten: str,
    so_cccd: str,
    so_dien_thoai: Optional[str] = None,
    dia_chi: Optional[str] = None,
) -> User:
    """Register a new citizen account."""
    # Check unique email
    existing = await user_repo.get_by_email(db, email)
    if existing:
        raise ConflictException(code="EMAIL_EXISTS", message="Email đã được đăng ký")

    # Check unique CCCD
    existing_cccd = await user_repo.get_by_cccd(db, so_cccd)
    if existing_cccd:
        raise ConflictException(code="CCCD_EXISTS", message="Số CCCD đã được đăng ký")

    user = await user_repo.create(
        db,
        obj_in={
            "id": uuid.uuid4(),
            "email": email,
            "password_hash": hash_password(password),
            "ho_ten": ho_ten,
            "so_cccd": so_cccd,
            "so_dien_thoai": so_dien_thoai,
            "dia_chi": dia_chi,
            "role": RoleEnum.citizen,
            "trang_thai": StatusEnum.active,
        },
    )
    return user


async def login(db: AsyncSession, email: str, password: str) -> dict:
    """Authenticate user and return JWT tokens."""
    user = await user_repo.get_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        raise UnauthorizedException("Email hoặc mật khẩu không đúng")

    if user.trang_thai != StatusEnum.active:
        raise UnauthorizedException("Tài khoản đã bị khoá")

    token_data = {"sub": str(user.id), "role": user.role.value}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    # Save refresh token to user record
    await user_repo.update(db, db_obj=user, obj_in={"refresh_token": refresh_token})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "id": str(user.id),
            "email": user.email,
            "ho_ten": user.ho_ten,
            "role": user.role.value,
        },
    }


async def refresh_token(db: AsyncSession, token: str) -> dict:
    """Issue a new token pair from a valid refresh token."""
    try:
        payload = decode_token(token)
        if payload.get("type") != "refresh":
            raise UnauthorizedException("Token không hợp lệ")
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token đã hết hạn")
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Token không hợp lệ")

    user = await user_repo.get(db, id=payload["sub"])
    if not user:
        raise UnauthorizedException("Người dùng không tồn tại")

    # Verify the refresh token matches what's stored
    if user.refresh_token != token:
        raise UnauthorizedException("Token đã được sử dụng")

    token_data = {"sub": str(user.id), "role": user.role.value}
    new_access = create_access_token(token_data)
    new_refresh = create_refresh_token(token_data)

    await user_repo.update(db, db_obj=user, obj_in={"refresh_token": new_refresh})

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


async def get_current_user(db: AsyncSession, user_id: str) -> User:
    """Get user by ID or raise."""
    user = await user_repo.get(db, id=user_id)
    if not user:
        raise UnauthorizedException("Người dùng không tồn tại")
    return user


async def change_password(
    db: AsyncSession, user: User, current_password: str, new_password: str
) -> None:
    """Change user password after verifying current password."""
    if not verify_password(current_password, user.password_hash):
        raise UnauthorizedException("Mật khẩu hiện tại không đúng")

    await user_repo.update(
        db, db_obj=user, obj_in={"password_hash": hash_password(new_password)}
    )


async def logout(db: AsyncSession, user: User) -> None:
    """Invalidate user's refresh token."""
    await user_repo.update(db, db_obj=user, obj_in={"refresh_token": None})
