import pytest
from src.database.repositories.thong_bao_repository import thong_bao_repo
from src.database.repositories.user_repository import user_repo
from src.models.thong_bao import LoaiThongBaoEnum

@pytest.mark.asyncio
async def test_create_thong_bao(db_session):
    # Lấy dữ liệu thật từ DB để tránh lỗi Foreign Key
    users = await user_repo.get_paginated(db_session, limit=1)
    user_id = users[0].id
    
    new_data = {
        "user_id": user_id,
        "tieu_de": "Test Thông Báo",
        "noi_dung": "Nội dung test",
        "loai": LoaiThongBaoEnum.he_thong,
        "da_doc": False
    }
    
    created = await thong_bao_repo.create(db_session, obj_in=new_data)
    assert created.id is not None
    assert created.tieu_de == "Test Thông Báo"
    assert created.da_doc is False
    
    # Update test
    updated = await thong_bao_repo.update(db_session, db_obj=created, obj_in={"da_doc": True})
    assert updated.da_doc is True
