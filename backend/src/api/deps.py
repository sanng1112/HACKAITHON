"""FastAPI dependency injection: database session, auth, current user."""
from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import get_db
from src.middleware.error_handler import UnauthorizedException
from src.services.auth_service import get_current_user as get_user_by_id
from src.config.settings import settings


async def get_current_user(
    authorization: str = Header(None, alias="Authorization"),
    db: AsyncSession = Depends(get_db),
):
    """Extract and validate JWT from Authorization header, return User."""
    if not authorization:
        raise UnauthorizedException("Thiếu token xác thực")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise UnauthorizedException("Token không hợp lệ")
    except ValueError:
        raise UnauthorizedException("Token không hợp lệ")

    import jwt as pyjwt
    from src.utils.security import decode_token

    try:
        payload = decode_token(token)
    except pyjwt.ExpiredSignatureError:
        raise UnauthorizedException("Token đã hết hạn")
    except pyjwt.InvalidTokenError:
        raise UnauthorizedException("Token không hợp lệ")

    user = await get_user_by_id(db, payload["sub"])
    if not user:
        raise UnauthorizedException("Người dùng không tồn tại")

    return user


async def require_role(*roles: str):
    """Dependency factory: require one of the specified roles."""
    async def role_checker(current_user=Depends(get_current_user)):
        if current_user.role.value not in roles:
            from src.middleware.error_handler import ForbiddenException
            raise ForbiddenException("Bạn không có quyền thực hiện hành động này")
        return current_user
    return role_checker
