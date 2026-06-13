import pytest
import uuid
from src.database.repositories.user_repository import user_repo
from src.models.user import RoleEnum

@pytest.mark.asyncio
async def test_get_by_email(db_session):
    # Test lấy admin đã được seed
    user = await user_repo.get_by_email(db_session, "admin@govone.vn")
    assert user is not None
    assert user.email == "admin@govone.vn"
    assert user.role == RoleEnum.admin

@pytest.mark.asyncio
async def test_create_user(db_session):
    # Tạo user ngẫu nhiên để test hàm Create
    test_email = f"test_{uuid.uuid4()}@govone.vn"
    new_user_data = {
        "email": test_email,
        "password_hash": "test_hash",
        "ho_ten": "Test User",
        "so_cccd": str(uuid.uuid4().int)[:12],
        "role": RoleEnum.citizen
    }
    
    created_user = await user_repo.create(db_session, obj_in=new_user_data)
    assert created_user.id is not None
    assert created_user.email == test_email
    assert created_user.ho_ten == "Test User"
    
    # Xóa user sau khi test xong để dọn dẹp
    deleted_user = await user_repo.delete(db_session, id=created_user.id)
    assert deleted_user is not None
