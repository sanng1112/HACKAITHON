import pytest
from src.database.repositories.ho_so_tai_lieu_repository import ho_so_tai_lieu_repo
from src.database.repositories.ho_so_repository import ho_so_repo

@pytest.mark.asyncio
async def test_create_and_get_tai_lieu(db_session):
    # Lấy dữ liệu thật từ DB để tránh lỗi Foreign Key
    ho_sos = await ho_so_repo.get_paginated_with_filters(db_session, limit=1)
    test_ho_so_id = ho_sos[0].id
    
    # Test Create
    new_data = {
        "ho_so_id": test_ho_so_id,
        "ten_file": "cccd_mat_truoc.jpg",
        "duong_dan": "/uploads/test.jpg",
        "loai_file": "image/jpeg",
        "kich_thuoc": 1024
    }
    
    created = await ho_so_tai_lieu_repo.create(db_session, obj_in=new_data)
    assert created.id is not None
    assert created.ho_so_id == test_ho_so_id
    
    # Test Get by ho so
    docs = await ho_so_tai_lieu_repo.get_by_ho_so(db_session, ho_so_id=test_ho_so_id)
    assert len(docs) >= 1
    assert docs[0].ten_file == "cccd_mat_truoc.jpg"
