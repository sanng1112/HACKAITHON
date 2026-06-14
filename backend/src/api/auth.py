"""Auth API router: register, login, refresh, me, change password, logout."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user, require_role
from src.database.connection import get_db
from src.models.user import User
from src.services import auth_service
from src.utils.response import success_response, error_response

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# ─── Schemas ────────────────────────────────────────────────

class RegisterInput(BaseModel):
    email: str
    password: str
    ho_ten: str
    so_cccd: str
    so_dien_thoai: str | None = None
    dia_chi: str | None = None


class LoginInput(BaseModel):
    email: str
    password: str


class RefreshInput(BaseModel):
    refresh_token: str


class ChangePasswordInput(BaseModel):
    current_password: str
    new_password: str


# ─── Endpoints ──────────────────────────────────────────────


@router.post("/register", status_code=201)
async def register(data: RegisterInput, db: AsyncSession = Depends(get_db)):
    """Register a new citizen account."""
    user = await auth_service.register(
        db=db,
        email=data.email,
        password=data.password,
        ho_ten=data.ho_ten,
        so_cccd=data.so_cccd,
        so_dien_thoai=data.so_dien_thoai,
        dia_chi=data.dia_chi,
    )
    return success_response({
        "id": str(user.id),
        "email": user.email,
        "ho_ten": user.ho_ten,
        "role": user.role.value,
        "created_at": user.created_at.isoformat(),
    })


@router.post("/login")
async def login(data: LoginInput, db: AsyncSession = Depends(get_db)):
    """Authenticate and return JWT tokens."""
    result = await auth_service.login(db=db, email=data.email, password=data.password)
    return success_response(result)


@router.post("/refresh")
async def refresh(data: RefreshInput, db: AsyncSession = Depends(get_db)):
    """Refresh access token using refresh token."""
    result = await auth_service.refresh_token(db=db, token=data.refresh_token)
    return success_response(result)


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return success_response({
        "id": str(current_user.id),
        "email": current_user.email,
        "ho_ten": current_user.ho_ten,
        "role": current_user.role.value,
        "so_cccd": current_user.so_cccd,
        "trang_thai": current_user.trang_thai.value,
    })


@router.post("/change-password")
async def change_password(
    data: ChangePasswordInput,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Change current user's password."""
    await auth_service.change_password(
        db=db, user=current_user,
        current_password=data.current_password,
        new_password=data.new_password,
    )
    return success_response({"message": "Đổi mật khẩu thành công"})


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Invalidate current refresh token."""
    await auth_service.logout(db=db, user=current_user)
    return success_response({"message": "Đăng xuất thành công"})
