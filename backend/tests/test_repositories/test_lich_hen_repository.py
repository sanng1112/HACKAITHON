import pytest
from datetime import date, time
from src.database.repositories.lich_hen_repository import lich_hen_repo
from src.database.repositories.user_repository import user_repo
from src.models.lich_hen import TrangThaiLichHenEnum

@pytest.mark.asyncio
async def test_create_and_delete_lich_hen(db_session):
    # Lấy dữ liệu thật từ DB để tránh lỗi Foreign Key
    users = await user_repo.get_paginated(db_session, limit=2)
    user_id = users[0].id
    can_bo_id = users[1].id
    
    new_data = {
        "user_id": user_id,
        "can_bo_id": can_bo_id,
        "tieu_de": "Test Lịch Hẹn",
        "ngay_hen": date(2026, 10, 10),
        "gio_hen": time(9, 0),
        "trang_thai": TrangThaiLichHenEnum.CHO_XAC_NHAN
    }
    
    created = await lich_hen_repo.create(db_session, obj_in=new_data)
    assert created.id is not None
    assert created.tieu_de == "Test Lịch Hẹn"
    
    fetched = await lich_hen_repo.get(db_session, id=created.id)
    assert fetched is not None
    assert fetched.user_id == user_id
    
    await lich_hen_repo.delete(db_session, id=created.id)
    fetched_after_delete = await lich_hen_repo.get(db_session, id=created.id)
    assert fetched_after_delete is None
