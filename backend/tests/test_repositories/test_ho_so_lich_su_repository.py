import pytest
from src.database.repositories.ho_so_lich_su_repository import ho_so_lich_su_repo
from src.database.repositories.user_repository import user_repo
from src.database.repositories.ho_so_repository import ho_so_repo

@pytest.mark.asyncio
async def test_create_and_get_by_ho_so(db_session):
    # Lấy dữ liệu thật từ DB để tránh lỗi Foreign Key
    users = await user_repo.get_paginated(db_session, limit=1)
    ho_sos = await ho_so_repo.get_paginated_with_filters(db_session, limit=1)
    test_ho_so_id = ho_sos[0].id
    user_id = users[0].id
    
    # Test Create
    new_data = {
        "ho_so_id": test_ho_so_id,
        "nguoi_thuc_hien_id": user_id,
        "hanh_dong": "Tạo mới",
        "ghi_chu": "Test lịch sử"
    }
    
    created = await ho_so_lich_su_repo.create(db_session, obj_in=new_data)
    assert created.id is not None
    assert created.ho_so_id == test_ho_so_id
    
    # Test Get by ho so
    history = await ho_so_lich_su_repo.get_by_ho_so(db_session, ho_so_id=test_ho_so_id)
    assert len(history) >= 1
    assert history[0].hanh_dong == "Tạo mới"
