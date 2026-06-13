import pytest
from src.database.repositories.ho_so_repository import ho_so_repo
from src.models.ho_so import TrangThaiHoSoEnum

@pytest.mark.asyncio
async def test_get_paginated_with_filters(db_session):
    # Test lấy danh sách hồ sơ (dữ liệu đã được seed 20 hồ sơ)
    danh_sach = await ho_so_repo.get_paginated_with_filters(db_session, skip=0, limit=5)
    assert len(danh_sach) == 5
    
    # Lấy thử 1 hồ sơ có trạng thái CHO_TIEP_NHAN
    danh_sach_cho_tiep_nhan = await ho_so_repo.get_paginated_with_filters(
        db_session, 
        skip=0, 
        limit=10, 
        trang_thai=TrangThaiHoSoEnum.CHO_TIEP_NHAN
    )
    
    if len(danh_sach_cho_tiep_nhan) > 0:
        assert danh_sach_cho_tiep_nhan[0].trang_thai == TrangThaiHoSoEnum.CHO_TIEP_NHAN
